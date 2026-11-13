import json
from typing import Dict, Any, List, Optional
from app.models.schemas_olympic import FullOlympicExam, OlympicQuestion, UserMatchConfig
from app.models.schemas_game import (
    AnswerSubmission,
    ScoreFeedback,
    DimensionScore,
    GameSessionSummary,
    HintRequest,
    HintResponse,
)

class PracticeAndArenaEngine:
    """
    Agent 4: Practice_&_Arena_Engine (Chuyên gia thiết kế cơ chế Chơi & Luyện tập)
    Quản lý 2 chế độ riêng biệt:
    1. Chế độ Thi đấu (ARENA_COMPETITION):
       - Khóa toàn bộ gợi ý
       - Đếm ngược nghiêm ngặt theo time_limit từng vòng (xác thực Backend chống gian lận)
       - Thưởng tốc độ, thưởng streak combo, cược Ngôi sao hy vọng
    2. Chế độ Luyện tập (PRACTICE_DOJO):
       - Không áp lực thời gian (đồng hồ tham khảo)
       - Mở khóa 2 tầng gợi ý (progressive_hints)
       - Trả về lời giải từng bước (step_by_step_explanation) ngay khi trả lời
       - Hỗ trợ làm lại câu hỏi hoặc tạo biến thể luyện tập
    """

    @staticmethod
    def evaluate_answer(
        submission: AnswerSubmission,
        question: OlympicQuestion,
        current_total_score: int,
        current_streak: int,
        match_mode: str = "ARENA_COMPETITION",
    ) -> ScoreFeedback:
        user_ans = submission.user_answer.strip().lower()
        correct_ans = question.correct_answer.strip().lower()

        # Kiểm tra tính đúng đắn
        is_correct = False
        if user_ans == correct_ans:
            is_correct = True
        elif question.acceptable_keywords:
            for kw in question.acceptable_keywords:
                if kw.strip().lower() in user_ans:
                    is_correct = True
                    break

        base_points = question.base_score
        speed_bonus = 0
        streak_bonus = 0
        star_multiplier = 1
        time_expired = False

        # Xác thực thời gian ở Backend đối với chế độ Thi đấu
        if match_mode == "ARENA_COMPETITION":
            # Cho phép dung sai mạng 2.5 giây
            if submission.time_taken_sec > (question.time_limit_sec + 2.5) or user_ans == "(hết thời gian)":
                is_correct = False
                time_expired = True

        if is_correct:
            new_streak = current_streak + 1

            if match_mode == "ARENA_COMPETITION":
                # Thưởng tốc độ chỉ áp dụng ở chế độ thi đấu
                time_left = max(0.0, question.time_limit_sec - submission.time_taken_sec)
                if question.time_limit_sec > 0:
                    speed_ratio = time_left / question.time_limit_sec
                    speed_bonus = int(speed_ratio * (base_points * 0.5))

                # Thưởng combo chuỗi đúng
                if new_streak > 0 and new_streak % 3 == 0:
                    streak_bonus = 10

                # Ngôi sao hy vọng
                if submission.star_of_hope_activated:
                    star_multiplier = 2
                    delta = (base_points * 2) + speed_bonus + streak_bonus
                else:
                    delta = base_points + speed_bonus + streak_bonus
            else:
                # Chế độ Luyện tập: Điểm tích lũy cơ bản không trừ điểm
                delta = base_points

            new_total = current_total_score + delta
        else:
            new_streak = 0
            if match_mode == "ARENA_COMPETITION" and submission.star_of_hope_activated:
                star_multiplier = -1
                delta = -base_points
            else:
                delta = 0
            new_total = max(0, current_total_score + delta)

        cit_dict = {
            "chunk_id": question.source_citation.chunk_id,
            "exact_quote": question.source_citation.exact_quote,
            "page_or_section": question.source_citation.page_or_section,
        }

        # Trong chế độ Luyện tập, luôn cung cấp step_by_step_explanation
        steps = question.step_by_step_explanation or [
            f"Bước 1: Nhận diện tiền đề trong tài liệu: '{question.source_citation.exact_quote[:80]}...'",
            f"Bước 2: Phân tích suy luận logic dẫn tới đáp án: '{question.correct_answer}'."
        ]

        feedback = ScoreFeedback(
            is_correct=is_correct,
            base_points=base_points if is_correct else 0,
            speed_bonus=speed_bonus,
            streak_bonus=streak_bonus,
            star_of_hope_multiplier=star_multiplier,
            total_delta_score=delta,
            current_total_score=new_total,
            current_streak=new_streak,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            step_by_step_explanation=steps,
            source_citation=cit_dict,
            time_expired=time_expired,
        )

        return feedback

    @staticmethod
    def get_hint(question: OlympicQuestion, hint_level: int, match_mode: str) -> HintResponse:
        """
        Lấy gợi ý 2 tầng trong chế độ Luyện tập. Khóa chặt nếu là Thi đấu.
        """
        if match_mode == "ARENA_COMPETITION":
            raise PermissionError("Chế độ Thi đấu Olympic khóa hoàn toàn chức năng xem gợi ý!")

        hints = question.progressive_hints
        if hint_level == 1:
            hint_text = hints.level_1_hint if hints else "Hãy liên hệ khái niệm nền tảng trong tài liệu."
            remaining = 1
        else:
            hint_text = hints.level_2_hint if hints else f"Đáp án liên quan chặt chẽ tới {question.source_citation.page_or_section}."
            remaining = 0

        return HintResponse(
            question_id=question.question_id,
            hint_level=hint_level,
            hint_text=hint_text,
            hints_remaining=remaining,
        )

    @staticmethod
    def generate_analytics(
        session_id: str,
        exam: FullOlympicExam,
        answer_logs: List[Dict[str, Any]],
        total_score: int,
        max_streak: int,
        time_spent: float,
        hints_used: int = 0,
        match_mode: str = "ARENA_COMPETITION",
    ) -> GameSessionSummary:
        q_map: Dict[str, OlympicQuestion] = {}
        for r in exam.rounds:
            for q in r.questions:
                q_map[q.question_id] = q

        dims = ["Concept", "Formula", "Causality", "EdgeCase", "Synthesis"]
        dim_stats = {d: {"total": 0, "correct": 0} for d in dims}

        for log in answer_logs:
            qid = log.get("question_id")
            q = q_map.get(qid)
            is_corr = log.get("is_correct", False)
            dim = q.knowledge_dimension if (q and q.knowledge_dimension in dim_stats) else "Concept"
            dim_stats[dim]["total"] += 1
            if is_corr:
                dim_stats[dim]["correct"] += 1

        dimension_scores: List[DimensionScore] = []
        strengths = []
        gaps = []

        dim_names_vn = {
            "Concept": "Nắm bắt Khái niệm Cốt lõi",
            "Formula": "Vận dụng Định lý & Công thức",
            "Causality": "Tư duy Nhân - Quả & Chuỗi biến cố",
            "EdgeCase": "Nhận diện Ngoại lệ & Điều kiện biên",
            "Synthesis": "Tổng hợp Đa bước & Phản biện",
        }

        for d in dims:
            t = dim_stats[d]["total"]
            c = dim_stats[d]["correct"]
            acc = round((c / t * 100), 1) if t > 0 else 100.0

            if acc >= 80:
                evaluation = "Thành thạo xuất sắc"
                strengths.append(f"{dim_names_vn[d]} ({acc}%)")
            elif acc >= 50:
                evaluation = "Khá tốt, cần củng cố thêm"
            else:
                evaluation = "Lỗ hổng kiến thức trọng tâm"
                gaps.append(f"{dim_names_vn[d]} (chỉ đạt {acc}%)")

            dimension_scores.append(
                DimensionScore(
                    dimension_name=dim_names_vn[d],
                    total_questions=t,
                    correct_count=c,
                    accuracy_percentage=acc,
                    evaluation=evaluation,
                )
            )

        recommendations = []
        if match_mode == "PRACTICE_DOJO":
            recommendations.append(f"Bạn đã sử dụng {hints_used} lượt gợi ý trong phiên luyện tập.")
            if hints_used == 0 and all(d.accuracy_percentage >= 70 for d in dimension_scores):
                recommendations.append("Năng lực rất vững! Bạn đã sẵn sàng chuyển sang Chế độ Thi đấu Olympic.")
            else:
                recommendations.append("Hãy luyện tập lại các câu hỏi thuộc phần điều kiện biên để tăng phản xạ.")
        else:
            if gaps:
                recommendations.append(f"Tập trung ôn luyện lại các phần: {', '.join(gaps)} qua Phòng Luyện tập Dojo.")
            if max_streak >= 5:
                recommendations.append("Tốc độ phản xạ và sự ổn định của bạn đạt chuẩn đấu trường Olympic.")

        return GameSessionSummary(
            session_id=session_id,
            document_title=exam.document_title,
            match_mode=match_mode,
            total_score=total_score,
            max_streak=max_streak,
            time_spent_sec=time_spent,
            hints_used_total=hints_used,
            dimension_analytics=dimension_scores,
            strengths=strengths or ["Tinh thần chủ động tiếp thu kiến thức"],
            knowledge_gaps=gaps or ["Nắm vững toàn diện tài liệu"],
            actionable_recommendations=recommendations,
        )

# Tương thích ngược
OlympicGameEngine = PracticeAndArenaEngine
