import json
import time
import random
import asyncio
from typing import Dict, List, Optional, Any
from starlette.websockets import WebSocket, WebSocketState
from pydantic import BaseModel

from app.models.schemas_olympic import FullOlympicExam, OlympicQuestion, UserMatchConfig
from app.services.game_engine import PracticeAndArenaEngine
from app.models.schemas_game import AnswerSubmission

class Player:
    def __init__(self, player_id: str, nickname: str, is_host: bool = False):
        self.player_id = player_id
        self.nickname = nickname
        self.is_host = is_host
        self.total_score = 0
        self.current_streak = 0
        self.max_streak = 0
        self.star_of_hope_activated = False
        self.is_connected = True
        self.ws: Optional[WebSocket] = None
        self.last_answer: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "nickname": self.nickname,
            "is_host": self.is_host,
            "total_score": self.total_score,
            "current_streak": self.current_streak,
            "max_streak": self.max_streak,
            "star_of_hope_activated": self.star_of_hope_activated,
            "is_connected": self.is_connected,
            "has_answered": self.last_answer is not None,
        }

class MultiplayerRoom:
    def __init__(
        self,
        room_code: str,
        host_player_id: str,
        document_id: str,
        document_title: str,
        exam: FullOlympicExam,
        config: UserMatchConfig,
    ):
        self.room_code = room_code
        self.host_player_id = host_player_id
        self.document_id = document_id
        self.document_title = document_title
        self.exam = exam
        self.config = config
        self.players: Dict[str, Player] = {}
        self.status: str = "LOBBY"  # LOBBY, IN_GAME, ROUND_OVER, FINISHED
        self.current_round_idx: int = 0
        self.current_question_idx: int = 0
        self.question_start_time: float = 0
        self.question_time_limit: int = 20
        self.answers_for_current_q: Dict[str, Dict[str, Any]] = {}
        self.timer_task: Optional[asyncio.Task] = None
        self.auto_advance_task: Optional[asyncio.Task] = None
        self.is_revealed: bool = False

    def get_current_question(self) -> Optional[OlympicQuestion]:
        if self.current_round_idx < len(self.exam.rounds):
            round_obj = self.exam.rounds[self.current_round_idx]
            if self.current_question_idx < len(round_obj.questions):
                return round_obj.questions[self.current_question_idx]
        return None

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (p.total_score, p.current_streak),
            reverse=True,
        )
        return [
            {
                "rank": idx + 1,
                "player_id": p.player_id,
                "nickname": p.nickname,
                "is_host": p.is_host,
                "total_score": p.total_score,
                "current_streak": p.current_streak,
                "max_streak": p.max_streak,
                "star_of_hope": p.star_of_hope_activated,
                "is_connected": p.is_connected,
            }
            for idx, p in enumerate(sorted_players)
        ]

class RoomManager:
    """
    Quản lý phòng đấu thời gian thực (Room_Manager)
    - Tạo mã phòng 6 ký tự OLY-XXX
    - Điều phối WebSocket broadcast đồng bộ
    - Xác thực thời gian nộp bài tại Server
    """

    def __init__(self):
        self.rooms: Dict[str, MultiplayerRoom] = {}

    def generate_room_code(self) -> str:
        while True:
            code = f"OLY-{random.randint(100, 999)}"
            if code not in self.rooms:
                return code

    def create_room(
        self,
        host_nickname: str,
        document_id: str,
        document_title: str,
        exam: FullOlympicExam,
        config: UserMatchConfig,
    ) -> (str, str):
        room_code = self.generate_room_code()
        host_player_id = f"PL_{random.randint(1000, 9999)}"
        host_player = Player(player_id=host_player_id, nickname=host_nickname, is_host=True)

        room = MultiplayerRoom(
            room_code=room_code,
            host_player_id=host_player_id,
            document_id=document_id,
            document_title=document_title,
            exam=exam,
            config=config,
        )
        room.players[host_player_id] = host_player
        self.rooms[room_code] = room
        return room_code, host_player_id

    def join_room(self, room_code: str, nickname: str, reconnect_player_id: Optional[str] = None) -> (str, MultiplayerRoom):
        room = self.rooms.get(room_code)
        if not room:
            raise ValueError(f"Không tìm thấy phòng thi với mã '{room_code}'")

        # Kiểm tra nếu reconnect lại với player_id cũ
        if reconnect_player_id and reconnect_player_id in room.players:
            player = room.players[reconnect_player_id]
            player.is_connected = True
            return reconnect_player_id, room

        # Không cho gia nhập mới khi phòng đã kết thúc
        if room.status == "FINISHED":
            raise ValueError("Phòng thi này đã kết thúc trận đấu.")

        # Tạo người chơi mới
        player_id = f"PL_{random.randint(1000, 9999)}"
        is_host = (len(room.players) == 0)
        player = Player(player_id=player_id, nickname=nickname, is_host=is_host)
        if is_host:
            room.host_player_id = player_id
        room.players[player_id] = player
        return player_id, room

    async def broadcast_to_room(self, room_code: str, message_type: str, payload: Dict[str, Any]):
        room = self.rooms.get(room_code)
        if not room:
            return

        data = {
            "type": message_type,
            "room_code": room_code,
            "timestamp": time.time(),
            "data": payload,
        }
        json_str = json.dumps(data, ensure_ascii=False)

        disconnected_players = []
        for p in list(room.players.values()):
            if p.ws and p.is_connected:
                try:
                    if p.ws.client_state == WebSocketState.CONNECTED:
                        await p.ws.send_text(json_str)
                except Exception:
                    p.is_connected = False
                    disconnected_players.append(p.player_id)

    async def start_game(self, room_code: str, host_player_id: str):
        room = self.rooms.get(room_code)
        if not room or room.host_player_id != host_player_id:
            raise PermissionError("Chỉ chủ phòng (Host) mới có quyền bắt đầu trận đấu!")

        room.status = "IN_GAME"
        room.current_round_idx = 0
        room.current_question_idx = 0
        await self.broadcast_next_question(room_code)

    start_match = start_game

    def _cancel_room_tasks(self, room: MultiplayerRoom):
        if room.timer_task and not room.timer_task.done():
            room.timer_task.cancel()
            room.timer_task = None
        if room.auto_advance_task and not room.auto_advance_task.done():
            room.auto_advance_task.cancel()
            room.auto_advance_task = None

    async def broadcast_next_question(self, room_code: str):
        room = self.rooms.get(room_code)
        if not room:
            return

        self._cancel_room_tasks(room)
        room.is_revealed = False

        current_q = room.get_current_question()
        if not current_q:
            # Hết câu hỏi -> Kết thúc trận đấu
            room.status = "FINISHED"
            await self.broadcast_to_room(room_code, "MATCH_FINISHED", {
                "leaderboard": room.get_leaderboard(),
                "document_title": room.document_title,
            })
            return

        # Reset câu trả lời của các người chơi cho câu hỏi mới
        room.answers_for_current_q.clear()
        for p in room.players.values():
            p.last_answer = None
            # Nếu không phải Vòng 4 thì reset cờ star_of_hope
            if current_q.round_number != 4:
                p.star_of_hope_activated = False

        current_round = room.exam.rounds[room.current_round_idx]
        room.question_start_time = time.time()
        room.question_time_limit = current_q.time_limit_sec

        # Ẩn đáp án đúng trước khi phát sóng cho các người chơi
        safe_q = current_q.model_dump()
        safe_q.pop("correct_answer", None)
        safe_q.pop("acceptable_keywords", None)
        safe_q.pop("explanation", None)
        safe_q.pop("step_by_step_explanation", None)
        safe_q.pop("progressive_hints", None)

        payload = {
            "round_number": current_round.round_number,
            "round_name": current_round.round_name,
            "round_theme": current_round.round_theme,
            "question_index": room.current_question_idx + 1,
            "total_questions_in_round": len(current_round.questions),
            "question": safe_q,
            "time_limit_sec": room.question_time_limit,
            "start_timestamp": room.question_start_time,
            "leaderboard": room.get_leaderboard(),
        }

        await self.broadcast_to_room(room_code, "QUESTION_START", payload)

        # Khởi động bộ đếm giờ tự động trên Server
        round_idx = room.current_round_idx
        q_idx = room.current_question_idx
        t_limit = room.question_time_limit
        room.timer_task = asyncio.create_task(
            self._question_timeout_watcher(room_code, round_idx, q_idx, t_limit)
        )

    async def _question_timeout_watcher(self, room_code: str, round_idx: int, q_idx: int, time_limit: int):
        """Watcher chạy ngầm trên Server: Hết giờ tự động nộp bài và công bố đáp án"""
        try:
            await asyncio.sleep(time_limit)
            room = self.rooms.get(room_code)
            if not room or room.status != "IN_GAME":
                return
            if room.current_round_idx != round_idx or room.current_question_idx != q_idx:
                return
            if room.is_revealed:
                return

            # Tự động nộp bài với kết quả time_expired cho tất cả người chơi chưa làm
            for p_id, p in list(room.players.items()):
                if p.is_connected and p_id not in room.answers_for_current_q:
                    try:
                        await self.handle_submit_answer(
                            room_code=room_code,
                            player_id=p_id,
                            user_answer="",
                            time_taken_sec=float(time_limit)
                        )
                    except Exception:
                        pass

            await self.reveal_question_results(room_code)
        except asyncio.CancelledError:
            pass

    async def _auto_advance_after_delay(self, room_code: str, delay: float = 2.5):
        """Tự động chuyển câu hỏi tiếp theo sau 2.5 giây công bố kết quả"""
        try:
            await asyncio.sleep(delay)
            room = self.rooms.get(room_code)
            if not room or room.status != "IN_GAME":
                return
            current_round = room.exam.rounds[room.current_round_idx]
            room.current_question_idx += 1
            if room.current_question_idx >= len(current_round.questions):
                room.current_round_idx += 1
                room.current_question_idx = 0
            await self.broadcast_next_question(room_code)
        except asyncio.CancelledError:
            pass

    async def handle_submit_answer(
        self,
        room_code: str,
        player_id: str,
        user_answer: str,
        time_taken_sec: float,
    ) -> Dict[str, Any]:
        room = self.rooms.get(room_code)
        if not room or room.status != "IN_GAME":
            raise ValueError("Phòng thi không ở trạng thái thi đấu.")

        player = room.players.get(player_id)
        if not player:
            raise ValueError("Người chơi không tồn tại trong phòng.")

        current_q = room.get_current_question()
        if not current_q:
            raise ValueError("Không có câu hỏi hiện hành.")

        # Kiểm tra nếu đã trả lời câu này rồi
        if player_id in room.answers_for_current_q:
            return room.answers_for_current_q[player_id]

        # Xác thực thời gian tại Server
        server_elapsed = time.time() - room.question_start_time
        verified_time_taken = min(time_taken_sec, server_elapsed)

        sub = AnswerSubmission(
            session_id=room_code,
            round_number=current_q.round_number,
            question_id=current_q.question_id,
            user_answer=user_answer,
            time_taken_sec=verified_time_taken,
            star_of_hope_activated=player.star_of_hope_activated,
            is_practice=False,
        )

        feedback = PracticeAndArenaEngine.evaluate_answer(
            submission=sub,
            question=current_q,
            current_total_score=player.total_score,
            current_streak=player.current_streak,
            match_mode="ARENA_COMPETITION",
        )

        player.total_score = feedback.current_total_score
        player.current_streak = feedback.current_streak
        if player.current_streak > player.max_streak:
            player.max_streak = player.current_streak

        result_data = {
            "player_id": player_id,
            "nickname": player.nickname,
            "is_correct": feedback.is_correct,
            "delta_score": feedback.total_delta_score,
            "current_total_score": player.total_score,
            "current_streak": player.current_streak,
            "speed_bonus": feedback.speed_bonus,
            "streak_bonus": feedback.streak_bonus,
            "correct_answer": feedback.correct_answer,
            "explanation": feedback.explanation,
            "source_citation": feedback.source_citation,
            "time_expired": feedback.time_expired,
        }

        player.last_answer = result_data
        room.answers_for_current_q[player_id] = result_data

        # Phát sóng thông báo người chơi đã nộp bài (giấu đáp án cho tới khi kết thúc câu)
        await self.broadcast_to_room(room_code, "PLAYER_SUBMITTED", {
            "player_id": player_id,
            "nickname": player.nickname,
            "has_answered": True,
            "answered_count": len(room.answers_for_current_q),
            "total_players": len(room.players),
        })

        # Nếu tất cả người chơi đang kết nối đều đã nộp bài, công bố kết quả câu hỏi ngay
        connected_count = sum(1 for p in room.players.values() if p.is_connected)
        if len(room.answers_for_current_q) >= connected_count and not room.is_revealed:
            await self.reveal_question_results(room_code)

        return result_data

    async def reveal_question_results(self, room_code: str):
        room = self.rooms.get(room_code)
        if not room or room.is_revealed:
            return

        room.is_revealed = True
        if room.timer_task and not room.timer_task.done():
            room.timer_task.cancel()
            room.timer_task = None

        current_q = room.get_current_question()
        if not current_q:
            return

        payload = {
            "question_id": current_q.question_id,
            "correct_answer": current_q.correct_answer,
            "explanation": current_q.explanation,
            "source_citation": {
                "chunk_id": current_q.source_citation.chunk_id,
                "exact_quote": current_q.source_citation.exact_quote,
                "page_or_section": current_q.source_citation.page_or_section,
            },
            "answers_summary": room.answers_for_current_q,
            "leaderboard": room.get_leaderboard(),
            "auto_advance_seconds": 2.5,
        }

        await self.broadcast_to_room(room_code, "QUESTION_RESULT", payload)

        # Tự động phát sóng câu hỏi tiếp theo sau 2.5s
        room.auto_advance_task = asyncio.create_task(
            self._auto_advance_after_delay(room_code, delay=2.5)
        )

    async def next_question_host(self, room_code: str, host_player_id: str):
        room = self.rooms.get(room_code)
        if not room or room.host_player_id != host_player_id:
            raise PermissionError("Chỉ chủ phòng mới có quyền chuyển câu hỏi!")

        self._cancel_room_tasks(room)

        current_round = room.exam.rounds[room.current_round_idx]
        room.current_question_idx += 1

        if room.current_question_idx >= len(current_round.questions):
            room.current_round_idx += 1
            room.current_question_idx = 0

        await self.broadcast_next_question(room_code)

    async def toggle_star_of_hope(self, room_code: str, player_id: str) -> bool:
        room = self.rooms.get(room_code)
        if not room:
            return False

        player = room.players.get(player_id)
        if not player:
            return False

        player.star_of_hope_activated = not player.star_of_hope_activated
        await self.broadcast_to_room(room_code, "STAR_OF_HOPE_TOGGLED", {
            "player_id": player_id,
            "nickname": player.nickname,
            "is_activated": player.star_of_hope_activated,
            "leaderboard": room.get_leaderboard(),
        })
        return player.star_of_hope_activated

# Khởi tạo singleton room manager
multiplayer_manager = RoomManager()

