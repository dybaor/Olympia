import os
import unittest
from pathlib import Path

from app.services.md_quiz_parser import DirectMDQuizParser
from app.models.schemas_olympic import UserMatchConfig, RoundConfig

class TestDirectMDQuizParser(unittest.TestCase):
    def setUp(self):
        self.sample_path = Path("dist/Olympic_Portable/data/uploads/DOC_d7d53406_annamluccu.md")
        if not self.sample_path.exists():
            matches = list(Path(".").glob("**/*annamluccu.md"))
            if matches:
                self.sample_path = matches[0]

    def test_01_auto_detection(self):
        """Kiểm tra khả năng tự động nhận diện file Markdown bộ đề trắc nghiệm vs văn bản lý thuyết"""
        self.assertTrue(self.sample_path.exists(), f"Không tìm thấy file mẫu tại {self.sample_path}")
        content = self.sample_path.read_text(encoding="utf-8")
        
        self.assertTrue(DirectMDQuizParser.is_markdown_quiz(content))

        theory_content = """# GIÁO TRÌNH MẠNG MÁY TÍNH
        Chương 1 giới thiệu về mạng Internet, kiến trúc phân tầng, chuyển mạch gói và chuyển mạch kênh.
        Không có câu hỏi và đáp án A, B, C, D ở đây.
        """
        self.assertFalse(DirectMDQuizParser.is_markdown_quiz(theory_content))
        print("  ✓ Test 1: Tự động nhận diện định dạng (Auto-Detection) PASSED!")

    def test_02_parse_all_300_questions(self):
        """Bóc tách chính xác 300 câu hỏi và xác thực cấu trúc dữ liệu"""
        content = self.sample_path.read_text(encoding="utf-8")
        questions, topics = DirectMDQuizParser.parse_document(content, "DOC_TEST", "Test Exam")

        self.assertEqual(len(questions), 300, f"Kỳ vọng 300 câu hỏi, nhận được {len(questions)}")
        self.assertEqual(len(topics), 3, f"Kỳ vọng 3 phần/chương, nhận được {len(topics)}")

        print(f"  ✓ Test 2: Bóc tách thành công {len(questions)}/300 câu hỏi từ {len(topics)} chuyên đề!")

    def test_03_options_and_correct_answers_integrity(self):
        """Kiểm tra 100% câu hỏi có đủ 4 lựa chọn, đáp án đúng sạch sẽ (không lộ dấu **)"""
        content = self.sample_path.read_text(encoding="utf-8")
        questions, _ = DirectMDQuizParser.parse_document(content, "DOC_TEST", "Test Exam")

        for idx, q in enumerate(questions):
            self.assertEqual(len(q.options), 4, f"Câu {idx+1} không có đủ 4 phương án: {q.options}")
            self.assertIn(q.correct_answer, q.options, f"Câu {idx+1}: Đáp án đúng '{q.correct_answer}' không nằm trong options: {q.options}")
            
            for opt in q.options:
                self.assertNotIn("**", opt, f"Câu {idx+1}: Phương án '{opt}' bị lộ dấu **")
                # Không được là tiêu đề câu hỏi rác
                self.assertFalse(opt.strip().lower() == "câu 181", f"Câu {idx+1}: Bị dính đáp án rác '{opt}'")
            self.assertNotIn("**", q.correct_answer, f"Câu {idx+1}: Đáp án đúng '{q.correct_answer}' bị lộ dấu **")

            self.assertTrue(len(q.explanation) > 5, f"Câu {idx+1} thiếu lời giải thích")
            self.assertTrue(len(q.progressive_hints.level_1_hint) > 10, f"Câu {idx+1} thiếu Gợi ý Cấp 1")
            self.assertTrue(len(q.progressive_hints.level_2_hint) > 10, f"Câu {idx+1} thiếu Gợi ý Cấp 2")

        print("  ✓ Test 3: Tính toàn vẹn 4 phương án, làm sạch dấu ** và 2 tầng gợi ý đạt 100%!")

    def test_04_no_synthetic_prompts_or_junk_distractors(self):
        """BẢO VỆ NGUYÊN BẢN: Cấm tuyệt đối sinh câu hỏi khuôn mẫu và cấm trộn đáp án rác"""
        content = self.sample_path.read_text(encoding="utf-8")
        bundle = DirectMDQuizParser.build_knowledge_bundle(content, "DOC_TEST", "Test Exam")
        exam = DirectMDQuizParser.build_olympic_exam(bundle, UserMatchConfig())

        for r in exam.rounds:
            for q in r.questions:
                # Tuyệt đối cấm câu hỏi khuôn mẫu
                self.assertNotIn("Thuật ngữ nào sau đây được định nghĩa là", q.prompt)
                for opt in q.options:
                    self.assertNotEqual(opt.strip().lower(), "câu 181")
                    self.assertFalse(opt.strip().lower().startswith("phần 1"))

        print("  ✓ Test 4: BẢO VỆ NGUYÊN BẢN 100% (Không câu hỏi khuôn mẫu, không đáp án rác 'Câu 181') PASSED!")

    def test_05_olympic_round_distribution(self):
        """Kiểm tra phân bổ câu hỏi vào 4 vòng thi Olympic theo tham số tùy chỉnh"""
        content = self.sample_path.read_text(encoding="utf-8")
        bundle = DirectMDQuizParser.build_knowledge_bundle(content, "DOC_TEST", "Test Exam")

        custom_config = UserMatchConfig(
            match_mode="ARENA_COMPETITION",
            round_configs=[
                RoundConfig(round_number=1, question_count=10, time_limit_sec=15),
                RoundConfig(round_number=2, question_count=6, time_limit_sec=20),
                RoundConfig(round_number=3, question_count=6, time_limit_sec=30),
                RoundConfig(round_number=4, question_count=5, time_limit_sec=45),
            ]
        )

        exam = DirectMDQuizParser.build_olympic_exam(bundle, custom_config)
        self.assertEqual(len(exam.rounds), 4)
        self.assertEqual(len(exam.rounds[0].questions), 10)
        self.assertEqual(len(exam.rounds[1].questions), 6)
        self.assertEqual(len(exam.rounds[2].questions), 6)
        self.assertEqual(len(exam.rounds[3].questions), 5)
        self.assertEqual(exam.total_questions, 27)

        for q in exam.rounds[3].questions:
            self.assertTrue(q.allows_star_of_hope)

        print("  ✓ Test 5: Phân bổ tham số hóa 4 vòng thi Olympic chuẩn xác 100%!")

    def test_06_practice_dojo_mode(self):
        """Kiểm tra Chế độ Luyện tập (Practice Dojo) với toàn bộ câu hỏi hoặc theo chương"""
        content = self.sample_path.read_text(encoding="utf-8")
        bundle = DirectMDQuizParser.build_knowledge_bundle(content, "DOC_TEST", "Test Exam")

        practice_config = UserMatchConfig(
            match_mode="PRACTICE_DOJO",
            practice_filter="ALL_ROUNDS",
            practice_order="sequential"
        )

        practice_exam = DirectMDQuizParser.build_olympic_exam(bundle, practice_config)
        self.assertGreater(practice_exam.total_questions, 50)
        self.assertEqual(practice_exam.match_mode, "PRACTICE_DOJO")
        print(f"  ✓ Test 6: Chế độ Luyện tập nạp thành công {practice_exam.total_questions} câu chia thành {len(practice_exam.rounds)} chặng!")

if __name__ == "__main__":
    unittest.main()
