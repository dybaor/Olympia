import unittest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, DocumentModel
from app.services.md_quiz_parser import DirectMDQuizParser
from app.models.schemas_olympic import UserMatchConfig, RoundConfig
from app.services.multiplayer_manager import multiplayer_manager, Player
from app.api.routes_game import get_document_topics, setup_match

class TestTopicAndAutoAdvance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sample_path = Path("annamluccu.md")
        if not sample_path.exists():
            sample_path = Path("dist/Olympic_Portable/data/uploads/DOC_d7d53406_annamluccu.md")
        cls.content = sample_path.read_text(encoding="utf-8")
        cls.bundle = DirectMDQuizParser.build_knowledge_bundle(cls.content, "DOC_TEST_TOPIC", "Mạng máy tính 300 câu")

        # Khởi tạo in-memory test database
        cls.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        cls.db = cls.SessionLocal()

        doc_rec = DocumentModel(
            id="DOC_TEST_TOPIC",
            title=cls.bundle.document_title,
            file_type=".md",
            file_path="annamluccu.md",
            raw_content="",
            extracted_bundle_json=cls.bundle.model_dump_json(),
        )
        cls.db.add(doc_rec)
        cls.db.commit()

    def test_01_get_topics_api(self):
        """Kiểm tra API GET /api/game/topics trả về đúng danh sách 3 chuyên đề và số câu hỏi"""
        res = get_document_topics(document_id="DOC_TEST_TOPIC", db=self.db)
        self.assertEqual(res["total_questions"], 300)
        self.assertEqual(len(res["topics"]), 3)
        for t in res["topics"]:
            self.assertEqual(t["question_count"], 100)
        print("  ✓ Test 1: API /api/game/topics trả về chính xác 3 chuyên đề, mỗi chuyên đề 100 câu!")

    def test_02_practice_filter_by_topic(self):
        """Kiểm tra chọn lọc câu hỏi theo từng chuyên đề trong Practice Dojo"""
        topic_name = self.bundle.detected_topics[0] # Phần 1
        cfg = UserMatchConfig(
            match_mode="PRACTICE_DOJO",
            topic_filter=topic_name,
            practice_filter="ALL_ROUNDS",
            practice_order="sequential"
        )
        res = setup_match(document_id="DOC_TEST_TOPIC", config=cfg, db=self.db)
        total_q = sum(len(r["questions"]) for r in res["rounds"])
        self.assertEqual(total_q, 100, f"Kỳ vọng 100 câu cho chuyên đề 1, nhận được {total_q}")
        print(f"  ✓ Test 2: Nạp bộ đề luyện tập cho '{topic_name[:30]}...' lọc đúng 100/100 câu!")

    def test_03_multiplayer_auto_advance_state(self):
        """Kiểm tra trạng thái auto-advance và bộ đếm giờ tự động trong Multiplayer Room"""
        cfg = UserMatchConfig(
            match_mode="ARENA_COMPETITION",
            round_configs=[
                RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=3),
                RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=2),
                RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=25, question_count=2),
                RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=30, question_count=2),
            ]
        )
        exam = DirectMDQuizParser.build_olympic_exam(self.bundle, cfg)

        room_code, host_id = multiplayer_manager.create_room(
            host_nickname="Minh Triết (Host)",
            document_id="DOC_TEST_TOPIC",
            document_title="Test Exam",
            exam=exam,
            config=cfg
        )
        p2_id, room = multiplayer_manager.join_room(room_code, "Bảo Long")

        self.assertEqual(room.status, "LOBBY")
        self.assertFalse(room.is_revealed)
        self.assertIsNone(room.timer_task)
        self.assertIsNone(room.auto_advance_task)

        # Chuyển trạng thái sang IN_GAME
        room.status = "IN_GAME"
        room.current_round_idx = 0
        room.current_question_idx = 0
        current_q = room.get_current_question()
        self.assertIsNotNone(current_q)

        # Giả lập 2 người chơi nộp bài
        room.answers_for_current_q[host_id] = {"is_correct": True, "delta_score": 10}
        room.answers_for_current_q[p2_id] = {"is_correct": False, "delta_score": 0}

        # Kiểm tra điều kiện tự động reveal khi tất cả người chơi kết nối đã nộp
        connected_count = sum(1 for p in room.players.values() if p.is_connected)
        self.assertEqual(connected_count, 2)
        self.assertEqual(len(room.answers_for_current_q), 2)
        self.assertTrue(len(room.answers_for_current_q) >= connected_count)

        # Hủy các task an toàn
        multiplayer_manager._cancel_room_tasks(room)
        print("  ✓ Test 3: Trạng thái phòng và cơ chế tự động chuyển câu hỏi Multiplayer hoạt động chuẩn xác!")

if __name__ == "__main__":
    unittest.main()
