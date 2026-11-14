import unittest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, DocumentModel
from app.services.md_quiz_parser import DirectMDQuizParser
from app.models.schemas_olympic import UserMatchConfig, RoundConfig
from app.api.routes_game import get_document_topics, setup_match

class TestMultiFileQuizMerging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f1_content = """# PHẦN 1: GIAO THỨC TẦNG GIAO VẬN
#### **Câu 1:** TCP là giao thức gì?
A. Không tin cậy
B. **Hướng kết nối**
C. Không kết nối
D. Truyền tin không kiểm soát
**Đáp án đúng:** B
*Giải thích:* TCP là Transmission Control Protocol hướng kết nối tin cậy.

#### **Câu 2:** UDP có ưu điểm gì?
A. Kiểm soát luồng
B. Bắt tay 3 bước
C. **Nhanh và độ trễ thấp**
D. Truyền lại gói tin
**Đáp án đúng:** C
*Giải thích:* UDP không có overhead bắt tay nên nhanh.
"""

        cls.f2_content = """# PHẦN 2: TẦNG MẠNG VÀ ĐỊNH TUYẾN
#### **Câu 1:** Thiết bị tiêu biểu tầng mạng là gì?
A. Switch L2
B. Hub
C. **Router**
D. Repeater
**Đáp án đúng:** C
*Giải thích:* Router hoạt động ở tầng mạng IP.

#### **Câu 2:** Địa chỉ IPv4 có độ dài bao nhiêu?
A. 16 bit
B. **32 bit**
C. 64 bit
D. 128 bit
**Đáp án đúng:** B
*Giải thích:* IPv4 có độ dài 32 bit.
"""

        files_data = [
            {"filename": "viet69.md", "content": cls.f1_content},
            {"filename": "annamluccu.md", "content": cls.f2_content}
        ]

        cls.bundle = DirectMDQuizParser.build_merged_knowledge_bundle(
            files_data=files_data,
            doc_id="DOC_MERGED_TEST",
            combined_title="viet69.md + annamluccu.md"
        )

        cls.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=cls.engine)
        cls.SessionLocal = sessionmaker(bind=cls.engine)
        cls.db = cls.SessionLocal()

        doc_rec = DocumentModel(
            id="DOC_MERGED_TEST",
            title=cls.bundle.document_title,
            file_type="multi",
            file_path="viet69.md",
            raw_content="",
            extracted_bundle_json=cls.bundle.model_dump_json()
        )
        cls.db.add(doc_rec)
        cls.db.commit()

    def test_merged_questions_and_ids(self):
        """Kiểm tra tổng số câu hỏi và việc đánh số thứ tự liên tục MD_Q_001, MD_Q_002..."""
        self.assertEqual(self.bundle.total_direct_questions, 4)
        self.assertTrue(self.bundle.is_direct_quiz)
        
        # Tạo exam luyện tập
        cfg = UserMatchConfig(match_mode="PRACTICE_DOJO", topic_filter="ALL")
        exam = DirectMDQuizParser.build_olympic_exam(self.bundle, cfg)
        all_q = [q for r in exam.rounds for q in r.questions]
        self.assertEqual(len(all_q), 4)
        self.assertEqual(all_q[0].question_id, "MD_Q_001")
        self.assertEqual(all_q[1].question_id, "MD_Q_002")
        self.assertEqual(all_q[2].question_id, "MD_Q_003")
        self.assertEqual(all_q[3].question_id, "MD_Q_004")

    def test_topic_prefix_and_filtering(self):
        """Kiểm tra gắn nhãn file nguồn vào topic khi gộp nhiều file"""
        topics_res = get_document_topics(document_id="DOC_MERGED_TEST", db=self.db)
        topic_names = [t["topic_name"] for t in topics_res["topics"]]
        self.assertTrue(any("viet69.md" in t for t in topic_names))
        self.assertTrue(any("annamluccu.md" in t for t in topic_names))

        # Lọc đề chỉ lấy chủ đề thuộc viet69.md
        viet69_topic = [t for t in topic_names if "viet69.md" in t][0]
        cfg = UserMatchConfig(match_mode="PRACTICE_DOJO", topic_filter=viet69_topic)
        exam = DirectMDQuizParser.build_olympic_exam(self.bundle, cfg)
        filtered_q = [q for r in exam.rounds for q in r.questions]
        self.assertEqual(len(filtered_q), 2)
        self.assertIn("TCP", filtered_q[0].prompt)

    def test_competition_exam_generation(self):
        """Kiểm tra sinh đề thi đấu Olympic 4 vòng từ bundle gộp"""
        cfg = UserMatchConfig(
            match_mode="ARENA_COMPETITION",
            round_configs=[
                RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=1),
                RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=1),
                RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=25, question_count=1),
                RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=30, question_count=1),
            ]
        )
        exam = DirectMDQuizParser.build_olympic_exam(self.bundle, cfg)
        self.assertEqual(len(exam.rounds), 4)
        self.assertEqual(exam.total_questions, 4)

if __name__ == "__main__":
    unittest.main()
