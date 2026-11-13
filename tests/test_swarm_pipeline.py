import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.swarm_orchestrator import SwarmOrchestrator
from app.services.game_engine import PracticeAndArenaEngine
from app.models.schemas_olympic import UserMatchConfig, RoundConfig
from app.models.schemas_game import AnswerSubmission

def run_automated_test():
    print("=" * 75)
    print("🚀 BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN HỆ THỐNG 5 AGENTS (ARENA & PRACTICE DOJO)")
    print("=" * 75)

    sample_doc_path = BASE_DIR / "tests" / "sample_docs" / "kien_truc_he_thong_phan_tan_raft.md"
    assert sample_doc_path.exists(), f"Không tìm thấy file mẫu tại {sample_doc_path}"

    orchestrator = SwarmOrchestrator()

    # TEST 1: AGENT 1 - BÓC TÁCH & GẮN NHÃN PHÂN TẦNG BLOOM
    print("\n[TEST 1] Kích hoạt Agent 1: Bóc tách & Gắn nhãn thang tư duy Bloom...")
    bundle = orchestrator.parser.process_document(str(sample_doc_path))
    print(f"  ✓ Tổng số Chunks: {bundle.total_chunks}")
    
    bloom_levels = set()
    for d in bundle.concept_map.core_definitions:
        bloom_levels.add(d.bloom_level)
    for f in bundle.concept_map.formulas_and_theorems:
        bloom_levels.add(f.bloom_level)
    for e in bundle.concept_map.edge_cases:
        bloom_levels.add(e.bloom_level)
    
    print(f"  ✓ Các tầng nhận thức Bloom đã phát hiện: {bloom_levels}")
    assert "REMEMBER" in bloom_levels, "Thiếu tầng REMEMBER"
    assert "ANALYZE_EVALUATE" in bloom_levels, "Thiếu tầng ANALYZE_EVALUATE"

    # TEST 2: AGENT 2 - SINH ĐỀ THAM SỐ HÓA THEO CẤU HÌNH NGƯỜI DÙNG
    print("\n[TEST 2] Kích hoạt Agent 2: Kiến trúc đề thi tham số hóa (UserMatchConfig)...")
    custom_config = UserMatchConfig(
        match_mode="PRACTICE_DOJO",
        practice_filter="ALL_ROUNDS",
        round_configs=[
            RoundConfig(round_number=1, difficulty="EASY", time_limit_sec=10, question_count=4),
            RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=4),
            RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=35, question_count=4),
            RoundConfig(round_number=4, difficulty="EXTREME", time_limit_sec=50, question_count=3),
        ]
    )
    bundle, exam, critic_reports = orchestrator.execute_pipeline(
        str(sample_doc_path), match_config=custom_config
    )
    assert len(exam.rounds) == 4, "Đề thi phải đủ 4 vòng"
    assert exam.rounds[0].difficulty == "EASY"
    assert exam.rounds[3].difficulty == "EXTREME"
    print("  ✓ Đã sinh thành công 4 vòng thi theo đúng độ khó tham số hóa: EASY -> EXTREME.")

    # TEST 3: KIỂM TRA 2 TẦNG GỢI Ý & STEP-BY-STEP EXPLANATION
    print("\n[TEST 3] Kiểm tra cấu trúc Progressive Hints & Step-by-Step Explanation...")
    for r in exam.rounds:
        for q in r.questions:
            assert q.progressive_hints is not None, f"Câu {q.question_id} thiếu progressive_hints"
            assert len(q.progressive_hints.level_1_hint) > 10, f"Gợi ý tầng 1 câu {q.question_id} quá ngắn"
            assert len(q.progressive_hints.level_2_hint) > 10, f"Gợi ý tầng 2 câu {q.question_id} quá ngắn"
            assert len(q.step_by_step_explanation) >= 2, f"Câu {q.question_id} thiếu các bước suy luận"
            assert q.source_citation is not None
            assert len(q.source_citation.exact_quote) > 0

    print("  ✓ 100% câu hỏi đều có đầy đủ 2 tầng gợi ý và các bước suy luận logic từng bước.")

    # TEST 4: AGENT 3 - HỘI ĐỒNG THẨM ĐỊNH FACT CHECKER
    print("\n[TEST 4] Kiểm tra Thẩm định đối kháng của Agent 3...")
    for round_num, rep in critic_reports.items():
        assert rep.all_passed, f"Vòng {round_num} chưa được duyệt hoàn toàn"
        print(f"  ✓ Vòng {round_num}: Đã duyệt {rep.passed_count}/{len(rep.audit_results)} câu hỏi đạt chuẩn 100%.")

    # TEST 5: AGENT 4 - CƠ CHẾ THI ĐẤU OLYMPIC (ARENA) KHÓA GỢI Ý & PHẠT TIMEOUT
    print("\n[TEST 5] Kiểm tra Chế độ Thi đấu (ARENA_COMPETITION)...")
    q_test = exam.rounds[0].questions[0]
    
    # Thử lấy gợi ý trong chế độ thi đấu -> Bắt buộc ném ngoại lệ PermissionError
    try:
        PracticeAndArenaEngine.get_hint(q_test, hint_level=1, match_mode="ARENA_COMPETITION")
        assert False, "Lỗi bảo mật: Đã cho phép lấy gợi ý trong Chế độ Thi Đấu!"
    except PermissionError:
        print("  ✓ Chế độ Thi đấu: Khóa hoàn toàn chức năng xem gợi ý (Bảo mật thành công).")

    # Thử nộp bài quá giờ ở chế độ Thi đấu -> Bị tính timeout và 0 điểm
    sub_timeout = AnswerSubmission(
        session_id="SESS_TEST",
        round_number=1,
        question_id=q_test.question_id,
        user_answer=q_test.correct_answer,
        time_taken_sec=q_test.time_limit_sec + 10.0, # Trễ 10 giây
        star_of_hope_activated=False
    )
    fb_timeout = PracticeAndArenaEngine.evaluate_answer(
        sub_timeout, q_test, current_total_score=100, current_streak=3, match_mode="ARENA_COMPETITION"
    )
    assert not fb_timeout.is_correct, "Lỗi: Nộp bài trễ nhưng vẫn được tính đúng"
    assert fb_timeout.time_expired, "Lỗi: Không gắn cờ time_expired"
    print("  ✓ Chế độ Thi đấu: Xác thực thời gian ở Backend chống gian lận (Phạt hết giờ thành công).")

    # TEST 6: AGENT 4 - CƠ CHẾ LUYỆN TẬP (PRACTICE DOJO) MỞ KHÓA GỢI Ý & TẠO BIẾN THỂ
    print("\n[TEST 6] Kiểm tra Chế độ Luyện tập (PRACTICE_DOJO)...")
    # Lấy gợi ý cấp 1 và cấp 2 thành công
    h1 = PracticeAndArenaEngine.get_hint(q_test, hint_level=1, match_mode="PRACTICE_DOJO")
    h2 = PracticeAndArenaEngine.get_hint(q_test, hint_level=2, match_mode="PRACTICE_DOJO")
    assert len(h1.hint_text) > 0
    assert len(h2.hint_text) > 0
    print(f"  ✓ Lấy gợi ý Cấp 1: '{h1.hint_text}'")
    print(f"  ✓ Lấy gợi ý Cấp 2: '{h2.hint_text}'")

    # Nộp bài trong phòng Luyện tập -> Trả về step_by_step_explanation
    sub_practice = AnswerSubmission(
        session_id="SESS_PRACTICE",
        round_number=1,
        question_id=q_test.question_id,
        user_answer=q_test.correct_answer,
        time_taken_sec=5.0,
        is_practice=True
    )
    fb_practice = PracticeAndArenaEngine.evaluate_answer(
        sub_practice, q_test, current_total_score=0, current_streak=0, match_mode="PRACTICE_DOJO"
    )
    assert fb_practice.is_correct
    assert len(fb_practice.step_by_step_explanation) > 0
    print("  ✓ Chế độ Luyện tập: Trả về lời giải chi tiết từng bước ngay khi nộp bài.")

    # Tạo biến thể câu hỏi (Variant)
    architect = orchestrator.parser
    dyn_arch = exam
    from app.skills.round_architect import DynamicOlympicArchitect
    arch = DynamicOlympicArchitect(bundle)
    variant_q = arch.generate_question_variant(q_test)
    assert variant_q.question_id != q_test.question_id
    assert "_VAR_" in variant_q.question_id
    print(f"  ✓ Tạo thành công biến thể câu hỏi luyện tập: ID={variant_q.question_id}")

    print("\n" + "=" * 75)
    print("🎉 TẤT CẢ 6 BÀI KIỂM THỬ TỰ ĐỘNG ĐÃ VƯỢT QUA XUẤT SẮC (PASSED) 100%!")
    print("=" * 75)

if __name__ == "__main__":
    run_automated_test()
