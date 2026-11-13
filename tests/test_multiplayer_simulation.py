import json
import time
import sys
import asyncio
from pathlib import Path
from starlette.websockets import WebSocketState

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.models.schemas_olympic import UserMatchConfig, RoundConfig
from app.skills.doc_parser import KnowledgeGraphExtractor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, DocumentModel
from app.services.multiplayer_manager import multiplayer_manager, Player
from app.api.routes_multiplayer import create_room, join_room, CreateRoomRequest, JoinRoomRequest

# In-memory database độc lập hoàn toàn để không xung đột file lock với app đang chạy
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=test_engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

class MockWebSocket:
    """Mock WebSocket giả lập kết nối thời gian thực bằng asyncio.Queue"""
    def __init__(self, name: str):
        self.name = name
        self.queue = asyncio.Queue()
        self.client_state = WebSocketState.CONNECTED

    async def send_text(self, text: str):
        await self.queue.put(text)

    async def receive_json(self, timeout=3.0):
        try:
            raw = await asyncio.wait_for(self.queue.get(), timeout=timeout)
            return json.loads(raw)
        except asyncio.TimeoutError:
            return None

async def run_multiplayer_simulation():
    t_start = time.time()
    def log(msg):
        print(f"[{time.time() - t_start:.2f}s] {msg}", flush=True)

    log("=" * 70)
    log("🌐 BẮT ĐẦU KIỂM THỬ GIẢ LẬP 3 NGƯỜI CHƠI THI ĐẤU MULTIPLAYER")
    log("=" * 70)

    # 1. BÓC TÁCH TÀI LIỆU
    sample_doc_path = BASE_DIR / "tests" / "sample_docs" / "kien_truc_he_thong_phan_tan_raft.md"
    extractor = KnowledgeGraphExtractor()
    bundle = extractor.process_document(str(sample_doc_path), doc_id="DOC_MP_TEST")
    log("✓ Bóc tách tài liệu hoàn tất")

    db = TestSessionLocal()
    doc_rec = DocumentModel(
        id="DOC_MP_TEST",
        title=bundle.document_title,
        file_type=".md",
        file_path=str(sample_doc_path),
        raw_content="",
        extracted_bundle_json=bundle.model_dump_json(),
    )
    db.add(doc_rec)
    db.commit()
    log("✓ Lưu tài liệu vào in-memory db")

    # 2. CHỦ PHÒNG (HOST) TẠO PHÒNG QUA API ROUTE FUNCTION
    print("\n[BƯỚC 1] Chủ phòng ('Minh Triết - Host') tạo phòng thi đấu...")
    cfg = UserMatchConfig(
        match_mode="ARENA_COMPETITION",
        round_configs=[
            RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=3),
            RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=2),
            RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=25, question_count=2),
            RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=30, question_count=2),
        ]
    )

    create_req = CreateRoomRequest(
        host_nickname="Minh Triết (Host)",
        document_id="DOC_MP_TEST",
        config=cfg,
    )
    room_data = create_room(create_req, db=db)
    room_code = room_data["room_code"]
    host_id = room_data["host_player_id"]
    db.close()

    assert room_code.startswith("OLY-"), f"Mã phòng {room_code} không đúng định dạng OLY-XXX"
    print(f"  ✓ Đã kiến tạo phòng: {room_code} (Host ID: {host_id})")

    # 3. NGƯỜI CHƠI 2 & 3 GIA NHẬP QUA API ROUTE FUNCTION
    print("\n[BƯỚC 2] Người chơi 2 ('Bảo Long') và Người chơi 3 ('Thanh Hà') gia nhập...")
    j2 = join_room(JoinRoomRequest(room_code=room_code, nickname="Bảo Long"))
    p2_id = j2["player_id"]
    print(f"  ✓ Bảo Long đã vào phòng -> ID: {p2_id}")

    j3 = join_room(JoinRoomRequest(room_code=room_code, nickname="Thanh Hà"))
    p3_id = j3["player_id"]
    print(f"  ✓ Thanh Hà đã vào phòng -> ID: {p3_id}")

    # 4. KẾT NỐI WEBSOCKET ĐỒNG BỘ 3 NGƯỜI CHƠI
    print("\n[BƯỚC 3] Thiết lập kết nối 3 WebSockets đồng bộ vào phòng thi...")
    room = multiplayer_manager.rooms[room_code]
    ws_host = MockWebSocket("Host")
    ws_p2 = MockWebSocket("P2")
    ws_p3 = MockWebSocket("P3")

    room.players[host_id].ws = ws_host
    room.players[p2_id].ws = ws_p2
    room.players[p3_id].ws = ws_p3

    await multiplayer_manager.broadcast_to_room(room_code, "PLAYER_JOINED", {
        "player_id": p3_id,
        "nickname": "Thanh Hà",
        "total_players": len(room.players),
        "players": [p.to_dict() for p in room.players.values()],
        "leaderboard": room.get_leaderboard(),
    })

    msg_h = await ws_host.receive_json()
    msg_2 = await ws_p2.receive_json()
    msg_3 = await ws_p3.receive_json()

    assert msg_h["type"] == "PLAYER_JOINED"
    assert msg_2["type"] == "PLAYER_JOINED"
    assert msg_3["type"] == "PLAYER_JOINED"
    assert msg_h["data"]["total_players"] == 3
    print("  ✓ Cả 3 người chơi đã nhận broadcast danh sách phòng thời gian thực (3 người).")

    # 5. CHỦ PHÒNG BẮT ĐẦU TRẬN ĐẤU
    print("\n[BƯỚC 4] Chủ phòng bấm 'BẮT ĐẦU TRẬN ĐẤU' -> Đồng bộ phát sóng câu hỏi...")
    await multiplayer_manager.start_game(room_code, host_player_id=host_id)

    q_h = await ws_host.receive_json()
    q_2 = await ws_p2.receive_json()
    q_3 = await ws_p3.receive_json()

    assert q_h["type"] == "QUESTION_START"
    assert q_2["type"] == "QUESTION_START"
    assert q_3["type"] == "QUESTION_START"

    q_data = q_h["data"]["question"]
    print(f"  ✓ Cả 3 người chơi đồng thời nhận câu hỏi: '{q_data['prompt'][:60]}...'")
    print(f"  ✓ Giới hạn thời gian: {q_h['data']['time_limit_sec']}s (Mốc bắt đầu: {q_h['data']['start_timestamp']})")

    # 6. CẢ 3 NGƯỜI CHƠI NỘP ĐÁP ÁN VỚI TỐC ĐỘ VÀ KẾT QUẢ KHÁC NHAU
    print("\n[BƯỚC 5] Cả 3 người chơi nộp đáp án với tốc độ và câu trả lời khác nhau...")
    correct_ans = room.get_current_question().correct_answer

    # Host nộp đúng sau 2.0 giây
    await multiplayer_manager.handle_submit_answer(room_code, host_id, correct_ans, time_taken_sec=2.0)
    # P2 nộp đúng sau 5.0 giây
    await multiplayer_manager.handle_submit_answer(room_code, p2_id, correct_ans, time_taken_sec=5.0)
    # P3 nộp đáp án sai sau 7.0 giây
    await multiplayer_manager.handle_submit_answer(room_code, p3_id, "Đáp án sai hoàn toàn", time_taken_sec=7.0)

    # Sau khi người thứ 3 nộp, server tự động broadcast QUESTION_RESULT
    res_h = None
    for _ in range(10):
        m = await ws_host.receive_json()
        if m and m["type"] == "QUESTION_RESULT":
            res_h = m
            break

    assert res_h is not None, "Không nhận được sự kiện QUESTION_RESULT"
    print("  ✓ Cả 3 người đã nộp! Server tự động công bố kết quả và bảng xếp hạng trực tiếp:")

    leaderboard = res_h["data"]["leaderboard"]
    for p in leaderboard:
        print(f"     Hạng {p['rank']}: {p['nickname']} | Điểm: {p['total_score']} | Chuỗi: {p['current_streak']}")

    assert leaderboard[0]["player_id"] == host_id, "Host trả lời nhanh nhất phải đứng đầu"
    assert leaderboard[0]["total_score"] > leaderboard[1]["total_score"], "Host phải có điểm cao hơn do thưởng tốc độ"
    assert leaderboard[2]["total_score"] == 0, "P3 trả lời sai nhận 0 điểm"

    # 7. ĐẶT CƯỢC NGÔI SAO HY VỌNG
    print("\n[BƯỚC 6] Kiểm tra cơ chế Ngôi Sao Hy Vọng thời gian thực...")
    while not ws_host.queue.empty():
        ws_host.queue.get_nowait()

    await multiplayer_manager.toggle_star_of_hope(room_code, p2_id)
    star_msg = await ws_host.receive_json()
    assert star_msg["type"] == "STAR_OF_HOPE_TOGGLED"
    assert star_msg["data"]["nickname"] == "Bảo Long"
    assert star_msg["data"]["is_activated"] is True
    print("  ✓ Đã phát sóng thông báo: '⭐ Bảo Long ĐÃ ĐẶT CƯỢC NGÔI SAO HY VỌNG' tới cả phòng!")

    # 8. MẤT KẾT NỐI VÀ AUTO-RECONNECT
    print("\n[BƯỚC 7] Kiểm tra rớt mạng và kết nối lại (Auto-reconnect)...")
    rec_res = join_room(JoinRoomRequest(
        room_code=room_code,
        nickname="Bảo Long",
        reconnect_player_id=p2_id,
    ))
    assert rec_res["player_id"] == p2_id, "Phải giữ nguyên player_id cũ"
    assert room.players[p2_id].total_score > 0, "Điểm số phải được bảo toàn nguyên vẹn"
    print("  ✓ Bảo Long khôi phục kết nối thành công, bảo toàn điểm số và chuỗi thắng!")

    print("\n" + "=" * 75)
    print("🎉 HOÀN TẤT KIỂM THỬ GIẢ LẬP MULTIPLAYER: TẤT CẢ TÍNH NĂNG ĐẠT CHUẨN 100%!")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(run_multiplayer_simulation())
