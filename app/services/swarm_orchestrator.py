import copy
from typing import Dict, Any, Tuple
from app.models.schemas_extracted import ExtractedKnowledgeBundle
from app.models.schemas_olympic import FullOlympicExam, OlympicRoundSet, OlympicQuestion, UserMatchConfig, RoundConfig
from app.models.schemas_critic import CriticEvaluationReport
from app.skills.doc_parser import KnowledgeGraphExtractor, VIETNAMESE_STOPWORDS
from app.skills.round_architect import DynamicOlympicArchitect
from app.skills.fact_critic import AdversarialFactChecker
from app.core.config import MAX_RETRY_ATTEMPTS

class SwarmOrchestrator:
    """
    Nhạc trưởng điều phối (Swarm Orchestrator)
    Điều phối luồng công việc khép kín giữa 5 Agent:
    Agent 1 (Extractor) -> Agent 2 (Dynamic Architect) -> Agent 3 (Fact Checker)
    với tham số hóa cấu hình phòng thi đấu (UserMatchConfig) & vòng lặp phản biện tối đa 3 lần.
    """

    def __init__(self):
        self.parser = KnowledgeGraphExtractor()

    def execute_pipeline(
        self,
        file_path: str,
        doc_id: str = None,
        match_config: UserMatchConfig = None
    ) -> Tuple[ExtractedKnowledgeBundle, FullOlympicExam, Dict[int, CriticEvaluationReport]]:
        cfg = match_config or UserMatchConfig()
        cfg_map: Dict[int, RoundConfig] = {rc.round_number: rc for rc in cfg.round_configs}

        # BƯỚC 1: Kiểm tra tự động Fast-Import đối với file Markdown bộ đề trắc nghiệm
        from pathlib import Path
        ext = Path(file_path).suffix.lower()
        if ext in [".md", ".txt"]:
            try:
                from app.services.md_quiz_parser import DirectMDQuizParser
                content = Path(file_path).read_text(encoding="utf-8")
                if DirectMDQuizParser.is_markdown_quiz(content):
                    knowledge_bundle = DirectMDQuizParser.build_knowledge_bundle(
                        content, doc_id=doc_id or "DOC_MD", doc_title=Path(file_path).name
                    )
                    full_exam = DirectMDQuizParser.build_olympic_exam(knowledge_bundle, cfg)
                    return knowledge_bundle, full_exam, {}
            except Exception:
                pass

        # Kích hoạt Agent 1 bóc tách tri thức & phân tầng Bloom
        knowledge_bundle = self.parser.process_document(file_path, doc_id=doc_id)

        # BƯỚC 2: Khởi tạo Agent 2 và Agent 3
        architect = DynamicOlympicArchitect(knowledge_bundle)
        critic = AdversarialFactChecker(knowledge_bundle)

        final_rounds = []
        critic_reports: Dict[int, CriticEvaluationReport] = {}

        # BƯỚC 3: Sinh cuốn chiếu theo cấu hình từng vòng thi
        generators = [
            (1, lambda: architect.generate_round_1_khoi_dong(cfg_map.get(1))),
            (2, lambda: architect.generate_round_2_vuot_chuong_ngai_vat(cfg_map.get(2))),
            (3, lambda: architect.generate_round_3_tang_toc(cfg_map.get(3))),
            (4, lambda: architect.generate_round_4_ve_dich(cfg_map.get(4))),
        ]

        for round_num, gen_func in generators:
            attempt = 0
            best_round_set: OlympicRoundSet = gen_func()
            report: CriticEvaluationReport = critic.audit_round(best_round_set, retry_attempt=attempt)

            # Vòng lặp phản biện đối kháng (tối đa 3 lần)
            while not report.all_passed and attempt < MAX_RETRY_ATTEMPTS:
                attempt += 1
                revised_questions = []
                audit_map = {r.question_id: r for r in report.audit_results}

                for q in best_round_set.questions:
                    audit = audit_map.get(q.question_id)
                    if audit and audit.status == "REJECTED_NEEDS_REVISION":
                        revised_q = self._repair_question(q, audit.remedy_instruction, knowledge_bundle)
                        revised_questions.append(revised_q)
                    else:
                        revised_questions.append(q)

                best_round_set.questions = revised_questions
                report = critic.audit_round(best_round_set, retry_attempt=attempt)

            critic_reports[round_num] = report
            final_rounds.append(best_round_set)

        full_exam = FullOlympicExam(
            document_id=knowledge_bundle.document_id,
            document_title=knowledge_bundle.document_title,
            match_mode=cfg.match_mode,
            rounds=final_rounds,
            total_questions=sum(len(r.questions) for r in final_rounds),
        )

        return knowledge_bundle, full_exam, critic_reports

    def _repair_question(self, q: OlympicQuestion, remedy: str, bundle: ExtractedKnowledgeBundle) -> OlympicQuestion:
        fixed_q = copy.deepcopy(q)
        if fixed_q.options:
            clean_opts = []
            seen = set()
            for opt in fixed_q.options:
                cleaned = opt.strip()
                lower_c = cleaned.lower()
                # Loại bỏ từ nối, hư từ hoặc placeholder rác
                if lower_c in VIETNAMESE_STOPWORDS or any(p in lower_c for p in ["phương án phụ", "gợi ý phụ", "lựa chọn đối sánh", "phương án thay thế", "khái niệm phụ"]):
                    continue
                if cleaned not in seen and len(cleaned) >= 2:
                    clean_opts.append(cleaned)
                    seen.add(cleaned)

            # Đảm bảo đáp án đúng luôn có trong options
            if fixed_q.correct_answer not in seen:
                clean_opts.insert(0, fixed_q.correct_answer)
                seen.add(fixed_q.correct_answer)

            # Điền thêm từ các thuật ngữ chuyên ngành thật trong tài liệu nếu thiếu options
            source_candidates = (
                getattr(bundle.concept_map, "domain_glossary", [])
                + [d.term for d in bundle.concept_map.core_definitions]
                + bundle.detected_topics
            )
            for cand in source_candidates:
                cand_clean = cand.strip()
                if cand_clean not in seen and cand_clean.lower() not in VIETNAMESE_STOPWORDS and len(cand_clean) >= 2:
                    clean_opts.append(cand_clean)
                    seen.add(cand_clean)
                    if len(clean_opts) >= 4:
                        break

            fixed_q.options = clean_opts[:4]

        chunks_map = {c.chunk_id: c for c in bundle.chunks}
        cit = fixed_q.source_citation
        if cit.chunk_id not in chunks_map or not cit.exact_quote or cit.exact_quote.lower() not in chunks_map[cit.chunk_id].content.lower():
            target_chunk = chunks_map.get(cit.chunk_id) or (bundle.chunks[0] if bundle.chunks else None)
            if target_chunk:
                fixed_q.source_citation.chunk_id = target_chunk.chunk_id
                fixed_q.source_citation.page_or_section = target_chunk.page_or_section
                sentences = [s.strip() for s in target_chunk.content.split(".") if len(s.strip()) > 20]
                fixed_q.source_citation.exact_quote = sentences[0] if sentences else target_chunk.content[:100]

        return fixed_q
