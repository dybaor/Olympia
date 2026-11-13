import re
from typing import Dict, List, Tuple
from app.models.schemas_extracted import ExtractedKnowledgeBundle, ChunkMetadata
from app.models.schemas_olympic import OlympicQuestion, OlympicRoundSet
from app.models.schemas_critic import (
    QuestionAuditScore,
    QuestionAuditResult,
    CriticEvaluationReport,
)
from app.skills.doc_parser import VIETNAMESE_STOPWORDS

class AdversarialFactChecker:
    """
    Agent 3: Adversarial_Fact_Checker (Hội đồng Thẩm định & Phản biện)
    Kiểm tra chéo 100% câu hỏi do Agent 2 tạo ra với tài liệu gốc.
    Phát hiện ảo giác (hallucination), kiểm định chất lượng 2 tầng gợi ý,
    chống copy nguyên văn và đảm bảo phân loại độ khó chính xác.
    """

    def __init__(self, bundle: ExtractedKnowledgeBundle):
        self.bundle = bundle
        self.chunks_map: Dict[str, ChunkMetadata] = {c.chunk_id: c for c in bundle.chunks}

    def verify_citation_fidelity(self, question: OlympicQuestion) -> Tuple[float, bool, str]:
        cit = question.source_citation
        if not cit or not cit.chunk_id:
            return 0.0, True, "Thiếu trường trích dẫn source_citation hoặc chunk_id."

        chunk = self.chunks_map.get(cit.chunk_id)
        if not chunk:
            return 10.0, True, f"chunk_id '{cit.chunk_id}' không tồn tại trong danh sách phân đoạn của tài liệu."

        raw_quote = cit.exact_quote.strip().lower()
        chunk_content = chunk.content.lower()

        clean_quote = re.sub(r"[^\w\s]", "", raw_quote)
        clean_chunk = re.sub(r"[^\w\s]", "", chunk_content)

        if clean_quote in clean_chunk or any(w in clean_chunk for w in clean_quote.split()[:5]):
            fidelity = 95.0
            hallucination = False
            notes = "Trích dẫn chuẩn xác, khớp với nội dung phân đoạn gốc."
        else:
            found_elsewhere = False
            for other_id, other_chunk in self.chunks_map.items():
                if clean_quote in re.sub(r"[^\w\s]", "", other_chunk.content.lower()):
                    found_elsewhere = True
                    break

            if found_elsewhere:
                fidelity = 75.0
                hallucination = False
                notes = "Trích dẫn có trong tài liệu nhưng bị lệch chunk_id."
            else:
                fidelity = 30.0
                hallucination = True
                notes = "Ảo giác (Hallucination): Không tìm thấy căn cứ trích dẫn trong tài liệu."

        return fidelity, hallucination, notes

    def evaluate_distractors_and_hints(self, question: OlympicQuestion) -> Tuple[float, float, bool, bool, str]:
        distractor_score = 90.0
        clarity_score = 90.0
        is_verbatim = False
        is_ambiguous = False
        notes = []

        # 1. Kiểm tra options
        if question.options:
            opts = [o.strip() for o in question.options]
            if len(set(opts)) < len(opts):
                distractor_score -= 40
                is_ambiguous = True
                notes.append("Có phương án trả lời bị trùng lặp nội dung.")

            for opt in opts:
                opt_lower = opt.lower()
                if opt_lower in VIETNAMESE_STOPWORDS:
                    distractor_score = 0.0
                    is_ambiguous = True
                    notes.append(f"Phương án '{opt}' là từ nối/hư từ không có nghĩa chuyên môn.")
                    break
                if len(opt) < 2 or any(p in opt_lower for p in ["phương án phụ", "gợi ý phụ", "lựa chọn đối sánh", "phương án thay thế", "khái niệm phụ"]):
                    distractor_score -= 50
                    is_ambiguous = True
                    notes.append("Phương án gây nhiễu sơ sài hoặc mang tính placeholder.")
                    break

            if question.correct_answer.strip().lower() in VIETNAMESE_STOPWORDS:
                clarity_score = 0.0
                is_ambiguous = True
                notes.append(f"Đáp án đúng '{question.correct_answer}' là từ nối/hư từ không hợp lệ!")

            if question.correct_answer not in opts:
                clarity_score -= 50
                is_ambiguous = True
                notes.append("Đáp án đúng không nằm trong danh sách các phương án lựa chọn!")

        # 2. Kiểm tra chất lượng progressive_hints
        hints = question.progressive_hints
        if not hints or not hints.level_1_hint or not hints.level_2_hint:
            clarity_score -= 20
            notes.append("Thiếu hoặc gợi ý 2 tầng chưa hoàn chỉnh.")
        elif hints.level_1_hint == hints.level_2_hint:
            clarity_score -= 15
            notes.append("Gợi ý tầng 1 và tầng 2 bị trùng lặp nội dung.")

        # 3. Kiểm tra copy nguyên văn
        cit = question.source_citation
        if cit and cit.exact_quote:
            clean_prompt = re.sub(r"[^\w\s]", "", question.prompt.lower())
            clean_quote = re.sub(r"[^\w\s]", "", cit.exact_quote.lower())
            if clean_quote in clean_prompt and len(clean_quote) > 80:
                is_verbatim = True
                clarity_score -= 20
                notes.append("Câu hỏi copy nguyên văn quá dài từ tài liệu mà chưa qua tái cấu trúc tư duy.")

        distractor_score = max(0.0, min(100.0, distractor_score))
        clarity_score = max(0.0, min(100.0, clarity_score))

        return distractor_score, clarity_score, is_verbatim, is_ambiguous, "; ".join(notes) or "Đạt chuẩn thẩm định."

    def audit_question(self, question: OlympicQuestion) -> QuestionAuditResult:
        fidelity, hallucination, cit_notes = self.verify_citation_fidelity(question)
        distractor, clarity, is_verbatim, is_ambiguous, opt_notes = self.evaluate_distractors_and_hints(question)

        cognitive_depth = 85.0
        if question.round_number == 3:
            cognitive_depth = 90.0 if question.question_type == "multi_hop_scenario" else 75.0
        elif question.round_number == 4:
            cognitive_depth = 95.0 if question.allows_star_of_hope else 80.0

        scores = QuestionAuditScore(
            citation_fidelity=fidelity,
            distractor_quality=distractor,
            clarity_and_unambiguity=clarity,
            cognitive_depth=cognitive_depth,
        )

        needs_revision = (
            hallucination
            or fidelity < 60.0
            or distractor < 60.0
            or clarity < 65.0
            or is_ambiguous
        )

        if needs_revision:
            status = "REJECTED_NEEDS_REVISION"
            reasons = []
            if hallucination or fidelity < 60.0:
                reasons.append("Phát hiện ảo giác hoặc sai lệch nguồn trích dẫn")
            if distractor < 60.0:
                reasons.append("Phương án gây nhiễu chưa đạt chuẩn chất lượng")
            if clarity < 65.0 or is_ambiguous:
                reasons.append("Câu hỏi hoặc đáp án mơ hồ, thiếu chính xác")

            remedy = (
                f"Yêu cầu Agent 2 tái tạo câu hỏi {question.question_id}: "
                f"Bám sát nội dung tại chunk '{question.source_citation.chunk_id}', "
                f"cung cấp 4 phương án phân biệt rõ ràng và progressive_hints chuẩn xác."
            )
        else:
            status = "APPROVED"
            reasons = ["Đáp ứng đầy đủ tiêu chuẩn kiểm định Olympic"]
            remedy = None

        return QuestionAuditResult(
            question_id=question.question_id,
            status=status,
            scores=scores,
            hallucination_detected=hallucination,
            is_verbatim_copy=is_verbatim,
            is_ambiguous=is_ambiguous,
            critic_notes=f"{cit_notes} | {opt_notes}",
            remedy_instruction=remedy,
        )

    def audit_round(self, round_set: OlympicRoundSet, retry_attempt: int = 0) -> CriticEvaluationReport:
        audit_results: List[QuestionAuditResult] = []
        for q in round_set.questions:
            result = self.audit_question(q)
            audit_results.append(result)

        passed_count = sum(1 for r in audit_results if r.status == "APPROVED")
        rejected_count = len(audit_results) - passed_count
        all_passed = (rejected_count == 0)

        verdict = (
            f"Vòng {round_set.round_number} ({round_set.round_name}) [{round_set.difficulty}]: "
            f"Đã duyệt {passed_count}/{len(audit_results)} câu hỏi. "
            f"{'TẤT CẢ ĐẠT CHUẨN.' if all_passed else f'Cần sửa đổi {rejected_count} câu hỏi.'}"
        )

        return CriticEvaluationReport(
            round_number=round_set.round_number,
            all_passed=all_passed,
            retry_attempt=retry_attempt,
            passed_count=passed_count,
            rejected_count=rejected_count,
            audit_results=audit_results,
            summary_verdict=verdict,
        )

# Tương thích ngược
AdversarialCriticAndFactChecker = AdversarialFactChecker
