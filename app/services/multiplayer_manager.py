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
        self.round1_history: Dict[str, Dict[str, Any]] = {}
        self.round1_start_scores: Dict[str, int] = {}
        self.r1_finished_players: set = set()
        self.r1_safe_questions: List[Dict[str, Any]] = []
        self.r1_total_time_limit: int = 0
        self.r1_start_time: float = 0
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
        # Vòng 1 diễn ra theo tốc độ cá nhân bất đồng bộ (Asynchronous Pacing)
        await self.start_round_1_async(room_code)

    start_match = start_game

    async def start_round_1_async(self, room_code: str):
        """Khởi động Vòng 1 Khởi Động: Chế độ cá nhân bất đồng bộ (Personal Pacing)"""
        room = self.rooms.get(room_code)
        if not room or not room.exam.rounds:
            return

        self._cancel_room_tasks(room)
        room.status = "IN_GAME"
        room.current_round_idx = 0
        room.current_question_idx = 0
        room.r1_finished_players = set()
        room.round1_history.clear()

        r1 = room.exam.rounds[0]
        # Bóc tách câu hỏi an toàn (giấu đáp án và giải thích)
        safe_questions = []
        for q in r1.questions:
            sq = q.model_dump()
            sq.pop("correct_answer", None)
            sq.pop("acceptable_keywords", None)
            sq.pop("explanation", None)
            sq.pop("step_by_step_explanation", None)
            sq.pop("progressive_hints", None)
            safe_questions.append(sq)

        room.r1_safe_questions = safe_questions
        # Tổng thời gian vòng 1 = tổng thời gian từng câu + 15 giây dự phòng
        room.r1_total_time_limit = sum(q.time_limit_sec for q in r1.questions) + 15
        room.r1_start_time = time.time()

        for p in room.players.values():
            p.last_answer = None

        payload = {
            "round_number": 1,
            "round_name": r1.round_name,
            "round_theme": r1.round_theme,
            "questions": safe_questions,
            "total_questions": len(safe_questions),
            "total_time_limit": room.r1_total_time_limit,
            "start_timestamp": room.r1_start_time,
            "leaderboard": room.get_leaderboard(),
        }
        await self.broadcast_to_room(room_code, "ROUND_1_ASYNC_START", payload)

        # Bộ đếm giờ tổng Vòng 1
        room.timer_task = asyncio.create_task(
            self._r1_timeout_watcher(room_code, room.r1_total_time_limit)
        )

    async def _r1_timeout_watcher(self, room_code: str, time_limit: int):
        try:
            await asyncio.sleep(time_limit)
            room = self.rooms.get(room_code)
            if not room or room.status != "IN_GAME" or room.current_round_idx != 0:
                return
            await self.finish_round_1(room_code)
        except asyncio.CancelledError:
            pass

    async def handle_r1_submit_question(
        self,
        room_code: str,
        player_id: str,
        question_id: str,
        question_index: int,
        user_answer: str,
        time_taken_sec: float,
    ) -> Dict[str, Any]:
        """Ghi nhận đáp án câu hỏi Vòng 1 của từng người chơi theo chế độ thi mù"""
        room = self.rooms.get(room_code)
        if not room or room.status != "IN_GAME":
            return {}

        player = room.players.get(player_id)
        if not player:
            return {}

        r1 = room.exam.rounds[0]
        # Tìm câu hỏi tương ứng
        target_q = None
        for q in r1.questions:
            if q.question_id == question_id:
                target_q = q
                break
        if not target_q and 0 <= question_index < len(r1.questions):
            target_q = r1.questions[question_index]

        if not target_q:
            return {}

        sub = AnswerSubmission(
            session_id=room_code,
            round_number=1,
            question_id=target_q.question_id,
            user_answer=user_answer,
            time_taken_sec=time_taken_sec,
            star_of_hope_activated=False,
            is_practice=False,
        )

        feedback = PracticeAndArenaEngine.evaluate_answer(
            submission=sub,
            question=target_q,
            current_total_score=player.total_score,
            current_streak=player.current_streak,
            match_mode="ARENA_COMPETITION",
        )

        player.total_score = feedback.current_total_score
        player.current_streak = feedback.current_streak
        if player.current_streak > player.max_streak:
            player.max_streak = player.current_streak

        if target_q.question_id not in room.round1_history:
            room.round1_history[target_q.question_id] = {}

        room.round1_history[target_q.question_id][player_id] = {
            "user_answer": user_answer,
            "is_correct": feedback.is_correct,
            "delta_score": feedback.total_delta_score,
            "time_expired": feedback.time_expired,
            "time_taken_sec": time_taken_sec,
        }

        # Phát sóng tiến độ cho cả phòng (không tiết lộ đúng/sai)
        await self.broadcast_to_room(room_code, "R1_PLAYER_PROGRESS", {
            "player_id": player_id,
            "nickname": player.nickname,
            "question_index": question_index + 1,
            "total_questions": len(r1.questions),
        })

        return {"status": "ok", "recorded": True}

    async def handle_r1_player_finished(self, room_code: str, player_id: str):
        """Khi một người chơi hoàn thành tất cả câu hỏi của Vòng 1"""
        room = self.rooms.get(room_code)
        if not room or room.status != "IN_GAME" or room.current_round_idx != 0:
            return

        room.r1_finished_players.add(player_id)
        player = room.players.get(player_id)
        nickname = player.nickname if player else "Đấu thủ"

        await self.broadcast_to_room(room_code, "R1_PLAYER_COMPLETED", {
            "player_id": player_id,
            "nickname": nickname,
            "finished_count": len(room.r1_finished_players),
            "total_players": sum(1 for p in room.players.values() if p.is_connected),
        })

        connected_ids = {p_id for p_id, p in room.players.items() if p.is_connected}
        if connected_ids and connected_ids.issubset(room.r1_finished_players):
            await self.finish_round_1(room_code)

    async def finish_round_1(self, room_code: str):
        """Kết thúc Vòng 1 và mở Bảng đối chiếu kết quả 5 cột cho toàn phòng"""
        room = self.rooms.get(room_code)
        if not room or room.status != "IN_GAME":
            return

        self._cancel_room_tasks(room)
        room.status = "ROUND_1_SUMMARY"
        await self.broadcast_round_1_summary(room_code)

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

    async def _auto_advance_after_delay(self, room_code: str, delay: float = 5.0):
        """Tự động chuyển câu hỏi tiếp theo sau khoảng delay công bố kết quả"""
        try:
            await asyncio.sleep(delay)
            room = self.rooms.get(room_code)
            if not room or room.status != "IN_GAME":
                return
            current_round = room.exam.rounds[room.current_round_idx]
            room.current_question_idx += 1
            if room.current_question_idx >= len(current_round.questions):
                if room.current_round_idx == 0:
                    # KẾT THÚC VÒNG 1: Chuyển sang màn hình Bảng tổng kết Vòng 1
                    room.status = "ROUND_1_SUMMARY"
                    await self.broadcast_round_1_summary(room_code)
                    return
                else:
                    room.current_round_idx += 1
                    room.current_question_idx = 0
            await self.broadcast_next_question(room_code)
        except asyncio.CancelledError:
            pass

    async def broadcast_round_1_summary(self, room_code: str):
        """Phát sóng Bảng đối chiếu kết quả Vòng 1 cho toàn phòng"""
        room = self.rooms.get(room_code)
        if not room:
            return
        r1 = room.exam.rounds[0]
        summary_rows = []
        for idx, q in enumerate(r1.questions):
            q_hist = room.round1_history.get(q.question_id, {})
            summary_rows.append({
                "stt": idx + 1,
                "question_id": q.question_id,
                "question_text": q.prompt,
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "player_results": q_hist
            })

        payload = {
            "round_number": 1,
            "round_name": "Khởi Động",
            "summary_table": summary_rows,
            "leaderboard": room.get_leaderboard(),
            "auto_advance_seconds": 15.0,
        }
        await self.broadcast_to_room(room_code, "ROUND_1_SUMMARY", payload)

        # Sau 15s tự động sang Vòng 2 nếu Host không bấm chuyển ngay
        room.auto_advance_task = asyncio.create_task(
            self._auto_advance_round_2(room_code, delay=15.0)
        )

    async def _auto_advance_round_2(self, room_code: str, delay: float = 15.0):
        try:
            await asyncio.sleep(delay)
            room = self.rooms.get(room_code)
            if not room or room.status != "ROUND_1_SUMMARY":
                return
            await self.start_round_2(room_code, room.host_player_id)
        except asyncio.CancelledError:
            pass

    async def start_round_2(self, room_code: str, host_player_id: str):
        """Chuyển từ Bảng tổng kết Vòng 1 sang Vòng 2 (Vượt chướng ngại vật)"""
        room = self.rooms.get(room_code)
        if not room:
            return
        if room.host_player_id != host_player_id:
            raise PermissionError("Chỉ chủ phòng mới có quyền chuyển sang Vòng 2!")
        self._cancel_room_tasks(room)
        room.status = "IN_GAME"
        room.current_round_idx = 1
        room.current_question_idx = 0
        await self.broadcast_next_question(room_code)

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

        # Lưu lại lịch sử câu trả lời cho Vòng 1 để tổng kết
        if current_q.round_number == 1:
            if current_q.question_id not in room.round1_history:
                room.round1_history[current_q.question_id] = {}
            room.round1_history[current_q.question_id][player_id] = {
                "user_answer": user_answer,
                "is_correct": feedback.is_correct,
                "delta_score": feedback.total_delta_score,
                "time_expired": feedback.time_expired,
                "time_taken_sec": verified_time_taken,
            }

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

        is_round_1 = (current_q.round_number == 1)

        if is_round_1:
            # VÒNG 1: CHẾ ĐỘ THI MÙ (KHÔNG LỘ ĐÁP ÁN ĐÚNG/SAI, TỰ ĐỘNG CHUYỂN NHANH SAU 1.5S)
            advance_delay = 1.5
            payload = {
                "round_number": 1,
                "is_blind": True,
                "question_id": current_q.question_id,
                "auto_advance_seconds": 1.5,
                "message": "Đã ghi nhận đáp án của tất cả đấu thủ!",
            }
        else:
            # VÒNG 2, 3, 4: HIỂN THỊ ĐÁP ÁN ĐÚNG, GIẢI THÍCH VÀ ĐẾM NGƯỢC 5 GIÂY
            advance_delay = 5.0
            payload = {
                "round_number": current_q.round_number,
                "is_blind": False,
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
                "auto_advance_seconds": 5.0,
            }

        await self.broadcast_to_room(room_code, "QUESTION_RESULT", payload)

        # Tự động phát sóng câu hỏi tiếp theo
        room.auto_advance_task = asyncio.create_task(
            self._auto_advance_after_delay(room_code, delay=advance_delay)
        )

    async def next_question_host(self, room_code: str, host_player_id: str):
        room = self.rooms.get(room_code)
        if not room or room.host_player_id != host_player_id:
            raise PermissionError("Chỉ chủ phòng mới có quyền chuyển câu hỏi!")

        self._cancel_room_tasks(room)

        if room.status == "ROUND_1_SUMMARY":
            await self.start_round_2(room_code, host_player_id)
            return

        current_round = room.exam.rounds[room.current_round_idx]
        room.current_question_idx += 1

        if room.current_question_idx >= len(current_round.questions):
            if room.current_round_idx == 0:
                room.status = "ROUND_1_SUMMARY"
                await self.broadcast_round_1_summary(room_code)
                return
            else:
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

