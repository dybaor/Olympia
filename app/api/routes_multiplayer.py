import json
import time
from typing import Optional, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db, DocumentModel
from app.models.schemas_extracted import ExtractedKnowledgeBundle
from app.models.schemas_olympic import UserMatchConfig
from app.skills.round_architect import DynamicOlympicArchitect
from app.skills.fact_critic import AdversarialFactChecker
from app.services.multiplayer_manager import multiplayer_manager

router = APIRouter(prefix="/api/multiplayer", tags=["multiplayer"])

class CreateRoomRequest(BaseModel):
    host_nickname: str
    document_id: str
    config: UserMatchConfig

class JoinRoomRequest(BaseModel):
    room_code: str
    nickname: str
    reconnect_player_id: Optional[str] = None

@router.post("/create-room")
def create_room(req: CreateRoomRequest, db: Session = Depends(get_db)):
    doc_record = db.query(DocumentModel).filter(DocumentModel.id == req.document_id).first()
    if not doc_record:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu gốc")

    bundle = ExtractedKnowledgeBundle.model_validate_json(doc_record.extracted_bundle_json)

    # Sinh đề thi chuẩn 4 vòng theo cấu hình host
    architect = DynamicOlympicArchitect(bundle)
    exam = architect.generate_full_olympic_exam(req.config)

    # Thẩm định qua Critic
    critic = AdversarialFactChecker(bundle)
    for r in exam.rounds:
        critic.audit_round(r)

    room_code, host_player_id = multiplayer_manager.create_room(
        host_nickname=req.host_nickname,
        document_id=req.document_id,
        document_title=exam.document_title,
        exam=exam,
        config=req.config,
    )

    return {
        "status": "success",
        "room_code": room_code,
        "host_player_id": host_player_id,
        "document_title": exam.document_title,
        "invite_url": f"/#join={room_code}",
    }

@router.post("/join-room")
def join_room(req: JoinRoomRequest):
    code = req.room_code.strip().upper()
    try:
        player_id, room = multiplayer_manager.join_room(
            room_code=code,
            nickname=req.nickname.strip(),
            reconnect_player_id=req.reconnect_player_id,
        )
        return {
            "status": "success",
            "room_code": code,
            "player_id": player_id,
            "nickname": req.nickname,
            "is_host": (player_id == room.host_player_id),
            "document_title": room.document_title,
            "room_status": room.status,
            "total_players": len(room.players),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/room/{room_code}")
def get_room_details(room_code: str):
    code = room_code.strip().upper()
    room = multiplayer_manager.rooms.get(code)
    if not room:
        raise HTTPException(status_code=404, detail="Không tìm thấy phòng thi đấu")

    return {
        "room_code": room.room_code,
        "status": room.status,
        "document_title": room.document_title,
        "host_player_id": room.host_player_id,
        "total_players": len(room.players),
        "players": [p.to_dict() for p in room.players.values()],
        "leaderboard": room.get_leaderboard(),
    }

@router.websocket("/ws/{room_code}/{player_id}")
async def websocket_multiplayer_endpoint(websocket: WebSocket, room_code: str, player_id: str):
    code = room_code.strip().upper()
    room = multiplayer_manager.rooms.get(code)
    if not room:
        await websocket.close(code=4004, reason="Phòng không tồn tại")
        return

    player = room.players.get(player_id)
    if not player:
        await websocket.close(code=4003, reason="Người chơi không thuộc phòng này")
        return

    await websocket.accept()
    player.ws = websocket
    player.is_connected = True

    # Phát thông báo có người tham gia / kết nối lại
    await multiplayer_manager.broadcast_to_room(code, "PLAYER_JOINED", {
        "player_id": player.player_id,
        "nickname": player.nickname,
        "is_host": player.is_host,
        "total_players": len(room.players),
        "players": [p.to_dict() for p in room.players.values()],
        "leaderboard": room.get_leaderboard(),
    })

    # Nếu vào phòng khi trận đấu đang diễn ra -> gửi trạng thái câu hỏi hiện tại ngay
    if room.status == "IN_GAME":
        current_q = room.get_current_question()
        if current_q:
            safe_q = current_q.model_dump()
            safe_q.pop("correct_answer", None)
            safe_q.pop("explanation", None)
            current_round = room.exam.rounds[room.current_round_idx]
            await websocket.send_text(json.dumps({
                "type": "QUESTION_RESUME",
                "room_code": code,
                "data": {
                    "round_number": current_round.round_number,
                    "round_name": current_round.round_name,
                    "question_index": room.current_question_idx + 1,
                    "total_questions_in_round": len(current_round.questions),
                    "question": safe_q,
                    "time_limit_sec": room.question_time_limit,
                    "elapsed_sec": max(0, int(time.time() - room.question_start_time)),
                    "leaderboard": room.get_leaderboard(),
                }
            }, ensure_ascii=False))

    try:
        while True:
            text = await websocket.receive_text()
            msg = json.loads(text)
            action = msg.get("action")

            if action == "START_GAME":
                await multiplayer_manager.start_game(code, host_player_id=player_id)

            elif action == "SUBMIT_ANSWER":
                ans = msg.get("answer", "")
                time_taken = float(msg.get("time_taken", 10.0))
                await multiplayer_manager.handle_submit_answer(
                    room_code=code,
                    player_id=player_id,
                    user_answer=ans,
                    time_taken_sec=time_taken,
                )

            elif action == "NEXT_QUESTION":
                await multiplayer_manager.next_question_host(code, host_player_id=player_id)

            elif action == "TOGGLE_STAR_OF_HOPE":
                await multiplayer_manager.toggle_star_of_hope(code, player_id=player_id)

    except WebSocketDisconnect:
        player.is_connected = False
        player.ws = None
        await multiplayer_manager.broadcast_to_room(code, "PLAYER_DISCONNECTED", {
            "player_id": player.player_id,
            "nickname": player.nickname,
            "leaderboard": room.get_leaderboard(),
        })
    except Exception as e:
        player.is_connected = False
        player.ws = None
