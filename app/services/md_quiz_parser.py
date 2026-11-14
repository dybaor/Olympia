import re
import json
import random
import copy
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

from app.models.schemas_olympic import (
    OlympicQuestion,
    OlympicRoundSet,
    FullOlympicExam,
    UserMatchConfig,
    RoundConfig,
    ProgressiveHints,
    SourceCitation,
    DifficultyLevel,
    BloomLevel,
    QuestionType
)
from app.models.schemas_extracted import (
    ExtractedKnowledgeBundle,
    ConceptMap,
    ChunkMetadata
)

CALCULATION_KEYWORDS = [
    "tính", "độ trễ", "thông lượng", "delay", "throughput", "cidr", "vlsm", 
    "chia mạng", "eui-64", "rút gọn", "subnet", "băng thông", "rtt", "bytes", 
    "mbps", "kbps", "ms", "/24", "/28", "/27", "/26", "/25", "/29", "/30",
    "transmission", "propagation", "hex", "địa chỉ mạng", "broadcast", "subnet mask",
    "dung lượng", "thời gian truyền", "kích thước", "băng tần"
]

class DirectMDQuizParser:
    """
    Bộ phân tích trắc nghiệm trực tiếp từ Markdown (Fast-Import Parser)
    Đảm bảo 100% nguyên bản câu hỏi và 4 lựa chọn (A, B, C, D) từ file .md,
    ngắt hoàn toàn luồng sinh khuôn mẫu hoặc tự tạo đáp án nhiễu.
    """

    @staticmethod
    def is_markdown_quiz(content: str) -> bool:
        """
        Kiểm tra xem nội dung tài liệu có phải là file bộ đề trắc nghiệm sẵn hay không.
        Điều kiện: Chứa các mẫu câu hỏi trắc nghiệm kèm các phương án A, B, C, D.
        """
        if not content:
            return False
        q_matches = re.findall(
            r'(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?Câu\s+\d+\s*[:\.]', 
            content, 
            re.IGNORECASE
        )
        opt_matches = re.findall(r'^\s*(?:\*\*)?[A-D][\.\)]\s*', content, re.M)
        return len(q_matches) >= 2 and len(opt_matches) >= 6

    @classmethod
    def parse_document(cls, content: str, doc_id: str, doc_title: str) -> Tuple[List[OlympicQuestion], List[str]]:
        """
        Bóc tách nguyên văn 100% từng khối câu hỏi (Block-by-block parsing):
        - question_text: Giữ nguyên văn toàn bộ sau dấu : (công thức, mã IP/Hex).
        - options: Lấy chính xác 4 phương án A, B, C, D gốc của chính câu đó.
        - correct_answer: Nhận diện phương án in đậm **...**, làm sạch dấu **.
        - explanation: Lấy nguyên văn nội dung sau 'Giải thích:'.
        """
        # 1. Quét toàn bộ tiêu đề Phần / Chương phân cấp (## PHẦN ... hoặc ### ...)
        section_matches = list(re.finditer(r'^(#{2,3})\s+(.+)$', content, re.M))
        sections = []
        for sm in section_matches:
            level = len(sm.group(1))
            sec_title = sm.group(2).strip()
            # Loại bỏ các ký tự markdown thừa
            sec_title = re.sub(r'^\*+|\*+$', '', sec_title).strip()
            sections.append({
                "level": level,
                "title": sec_title,
                "start": sm.start()
            })

        # 2. Quét block-by-block từng câu hỏi
        # Pattern nhận diện mở đầu một câu hỏi mới
        q_header_regex = re.compile(
            r'(?:^|\n)\s*(?:#{1,6}\s*)?(?:\*\*)?Câu\s+(\d+)\s*[:\.]\s*(?:\*\*)?\s*', 
            re.IGNORECASE
        )

        matches = list(q_header_regex.finditer(content))
        if not matches:
            return [], [], {}

        parsed_questions: List[OlympicQuestion] = []
        topics_found: set = set()
        topic_counts: Dict[str, int] = {}

        for idx, m in enumerate(matches):
            q_num = int(m.group(1))
            start_pos = m.end()
            # Khối kết thúc tại vị trí bắt đầu của câu hỏi kế tiếp hoặc cuối tài liệu
            end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
            q_block = content[start_pos:end_pos].strip()

            # Xác định Topic gần nhất phía trên câu hỏi (hỗ trợ phân cấp ## và ###)
            header_start_pos = m.start()
            current_topic = "Tổng quan kiến thức"
            last_major = ""
            last_sub = ""
            for s in sections:
                if s["start"] <= header_start_pos:
                    if s["level"] == 2:
                        last_major = s["title"]
                        last_sub = ""
                    elif s["level"] == 3:
                        last_sub = s["title"]
                else:
                    break

            if last_major and last_sub:
                current_topic = f"{last_major} - {last_sub}"
            elif last_major:
                current_topic = last_major
            elif last_sub:
                current_topic = last_sub

            topics_found.add(current_topic)
            topic_counts[current_topic] = topic_counts.get(current_topic, 0) + 1

            # Tách các dòng trong block của chính câu hỏi này
            block_lines = [l.strip() for l in q_block.splitlines() if l.strip()]
            if not block_lines:
                continue

            # A. BÓC TÁCH NỘI DUNG CÂU HỎI (PROMPT) NGUYÊN VĂN
            prompt_lines = []
            opt_start_idx = 0
            for line_idx, l in enumerate(block_lines):
                # Kiểm tra xem dòng này có phải là phương án A, B, C, D không
                if re.match(r'^(?:\*\*)?[A-D][\.\)]\s*', l):
                    opt_start_idx = line_idx
                    break
                prompt_lines.append(l)

            prompt_text = " ".join(prompt_lines).strip()
            # Loại bỏ dấu markdown thừa ở cuối prompt nếu có
            prompt_text = re.sub(r'  +$', '', prompt_text)

            # B. BÓC TÁCH 4 PHƯƠNG ÁN A, B, C, D CỦA CHÍNH CÂU HỎI ĐÓ
            options: List[str] = []
            correct_answer = ""
            correct_letter = "A"

            # Tìm 4 dòng phương án trong phạm vi câu hỏi
            for line in block_lines[opt_start_idx:]:
                opt_match = re.match(r'^\s*(\*\*)?([A-D])[\.\)]\s*(.*?)(?:\*\*)?\s*$', line)
                if opt_match:
                    is_bold = bool(opt_match.group(1))
                    letter = opt_match.group(2).upper()
                    raw_opt_text = opt_match.group(3).strip()

                    # Làm sạch dấu markdown ** ở nội dung phương án
                    clean_opt_text = re.sub(r'\*\*', '', raw_opt_text).strip()
                    formatted_opt = f"{letter}. {clean_opt_text}"
                    options.append(formatted_opt)

                    # Kiểm tra xem có phải đáp án đúng được in đậm hay không
                    if is_bold or line.startswith("**") or f"**{letter}." in line or f"**{letter})" in line:
                        correct_answer = formatted_opt
                        correct_letter = letter

                # Nếu gặp dòng giải thích thì dừng quét options
                if re.match(r'^(?:\*|\-)?\s*(?:\*\*)?Giải thích', line, re.IGNORECASE):
                    break

            # Fallback nếu không phát hiện đáp án in đậm
            if not correct_answer and options:
                correct_answer = options[0]
                correct_letter = "A"

            # C. BÓC TÁCH LỜI GIẢI THÍCH NGUYÊN VĂN
            explanation_match = re.search(
                r'(?:\*|\-)?\s*(?:\*\*)?Giải thích\s*[:\.]\s*(?:\*\*)?\s*(.*)', 
                q_block, 
                re.DOTALL
            )
            if explanation_match:
                # Lấy dòng giải thích đầu tiên hoặc nội dung hoàn chỉnh
                raw_expl = explanation_match.group(1).strip()
                # Cắt gọn nếu có phần heading lạc vào cuối block
                expl_lines = [el.strip() for el in raw_expl.splitlines() if el.strip()]
                clean_expl_lines = []
                for el in expl_lines:
                    if el.startswith("#"):
                        break
                    clean_expl_lines.append(el)
                explanation_text = " ".join(clean_expl_lines).strip()
            else:
                explanation_text = "Kiến thức đối chiếu theo tài liệu chuẩn."

            # D. PHÁT HIỆN BÀI TOÁN TÍNH TOÁN KỸ THUẬT
            combined_text = (prompt_text + " " + explanation_text).lower()
            is_calculation = any(kw in combined_text for kw in CALCULATION_KEYWORDS)

            difficulty: DifficultyLevel = "HARD" if is_calculation else "MEDIUM"
            bloom: BloomLevel = "APPLY" if is_calculation else "UNDERSTAND"
            dimension = "Calculation / Networking Math" if is_calculation else "Concept"

            # E. GỢI Ý TIẾN TRÌNH 2 TẦNG (PROGRESSIVE HINTS)
            hint_1 = f"💡 Gợi ý tư duy: Câu hỏi thuộc chủ đề '{current_topic}'. Hãy nhớ lại các nguyên lý cốt lõi của phần này."
            if is_calculation:
                hint_2 = f"🔍 Manh mối then chốt: Đây là bài toán tính toán kỹ thuật mạng. Chú ý các thông số đơn vị (bytes, bits, Mbps, ms) và áp dụng công thức liên quan."
            else:
                short_clue = explanation_text[:120] + "..." if len(explanation_text) > 120 else explanation_text
                hint_2 = f"🔍 Manh mối then chốt: {short_clue}"

            # Từ khóa chấp nhận khi chấm điểm
            clean_correct_body = correct_answer[3:].strip() if len(correct_answer) > 3 else correct_answer
            acceptable_kw = [
                correct_answer,
                correct_letter,
                f"{correct_letter}.",
                clean_correct_body
            ]

            olympic_q = OlympicQuestion(
                question_id=f"MD_Q_{q_num:03d}",
                round_number=1,
                question_type="speed_mcq",
                bloom_level=bloom,
                difficulty=difficulty,
                prompt=prompt_text,
                options=options,
                correct_answer=correct_answer,
                acceptable_keywords=acceptable_kw,
                explanation=explanation_text,
                step_by_step_explanation=[
                    f"Bước 1: Xác định phạm vi câu hỏi thuộc chuyên đề '{current_topic}'.",
                    f"Bước 2: Phân tích cơ chế và dữ kiện chuyên môn: {explanation_text}",
                    f"Bước 3: Kết luận phương án chính xác nguyên bản: {correct_answer}."
                ],
                progressive_hints=ProgressiveHints(
                    level_1_hint=hint_1,
                    level_2_hint=hint_2
                ),
                source_citation=SourceCitation(
                    chunk_id=f"MD_CHUNK_{q_num:03d}",
                    exact_quote=explanation_text[:250],
                    page_or_section=current_topic
                ),
                time_limit_sec=20,
                base_score=10,
                allows_star_of_hope=False,
                knowledge_dimension=dimension
            )
            parsed_questions.append(olympic_q)

        # Giữ thứ tự xuất hiện của các topic
        ordered_topics = []
        for q in parsed_questions:
            top = q.source_citation.page_or_section
            if top and top not in ordered_topics:
                ordered_topics.append(top)
        for t in topics_found:
            if t not in ordered_topics:
                ordered_topics.append(t)

        return parsed_questions, ordered_topics, topic_counts

    @classmethod
    def build_knowledge_bundle(cls, content: str, doc_id: str, doc_title: str) -> ExtractedKnowledgeBundle:
        """
        Nạp nhanh (Fast-Import) vào ExtractedKnowledgeBundle.
        TUYỆT ĐỐI KHÔNG tạo các CoreDefinition giả định để không bị luồng sinh khuôn mẫu gọi.
        """
        parse_res = cls.parse_document(content, doc_id, doc_title)
        if len(parse_res) == 3:
            questions, topics, topic_counts = parse_res
        else:
            questions, topics = parse_res
            topic_counts = {}

        chunks = [
            ChunkMetadata(
                chunk_id=f"CHUNK_{idx+1}",
                content=f"Chuyên đề: {top}",
                page_or_section=top,
                token_count_approx=len(content) // max(1, len(topics)),
                primary_bloom_level="UNDERSTAND"
            )
            for idx, top in enumerate(topics)
        ]

        bundle = ExtractedKnowledgeBundle(
            document_id=doc_id,
            document_title=doc_title,
            total_chunks=len(chunks),
            detected_topics=topics,
            chunks=chunks,
            concept_map=ConceptMap(
                core_definitions=[],
                formulas_and_theorems=[],
                causal_relationships=[],
                edge_cases=[],
                domain_glossary=[]
            ),
            is_direct_quiz=True,
            direct_quiz_questions_json=json.dumps([q.model_dump() for q in questions], ensure_ascii=False),
            direct_quiz_topics=topics,
            topic_question_counts=topic_counts,
            total_direct_questions=len(questions)
        )
        return bundle

    @classmethod
    def build_olympic_exam(
        cls, 
        bundle: ExtractedKnowledgeBundle, 
        config: UserMatchConfig
    ) -> FullOlympicExam:
        """
        Phân bổ câu hỏi nguyên bản 100% vào 4 vòng thi Olympic hoặc Chế độ Luyện tập.
        Tuyệt đối không viết lại câu hỏi, không tự chế thêm phương án nhiễu.
        """
        raw_questions_data = json.loads(bundle.direct_quiz_questions_json or "[]")
        all_questions = [OlympicQuestion.model_validate(item) for item in raw_questions_data]

        # 1. Lọc theo Topic / Phần nếu người dùng chọn
        filtered_questions = all_questions
        if config.topic_filter and config.topic_filter != "ALL":
            filtered_questions = [
                q for q in all_questions 
                if config.topic_filter.lower() in q.source_citation.page_or_section.lower()
            ]
            if not filtered_questions:
                filtered_questions = all_questions

        # 2. Chế độ Luyện tập (PRACTICE_DOJO)
        if config.match_mode == "PRACTICE_DOJO":
            return cls._build_practice_exam(filtered_questions, bundle, config)

        # 3. Chế độ Thi đấu Olympic (ARENA_COMPETITION / MULTIPLAYER)
        return cls._build_competition_exam(filtered_questions, bundle, config)

    @classmethod
    def _build_competition_exam(
        cls, 
        questions: List[OlympicQuestion], 
        bundle: ExtractedKnowledgeBundle, 
        config: UserMatchConfig
    ) -> FullOlympicExam:
        """Phân bổ vào 4 Vòng thi đấu Olympic từ các câu hỏi nguyên bản"""
        cfg_map = {rc.round_number: rc for rc in config.round_configs}
        cfg_r1 = cfg_map.get(1, RoundConfig(round_number=1, question_count=8, time_limit_sec=15))
        cfg_r2 = cfg_map.get(2, RoundConfig(round_number=2, question_count=4, time_limit_sec=20))
        cfg_r3 = cfg_map.get(3, RoundConfig(round_number=3, question_count=4, time_limit_sec=30))
        cfg_r4 = cfg_map.get(4, RoundConfig(round_number=4, question_count=3, time_limit_sec=45))

        # Phân nhóm: Nhóm khái niệm vs Nhóm tính toán
        conceptual_pool = [q for q in questions if "Calculation" not in q.knowledge_dimension]
        calculation_pool = [q for q in questions if "Calculation" in q.knowledge_dimension]

        # Trộn ngẫu nhiên câu hỏi để các trận thi đấu phong phú
        random.shuffle(conceptual_pool)
        random.shuffle(calculation_pool)

        # Fallback nếu thiếu câu tính toán
        if len(calculation_pool) < (cfg_r3.question_count + cfg_r4.question_count):
            extra_needed = (cfg_r3.question_count + cfg_r4.question_count) - len(calculation_pool)
            calculation_pool.extend(conceptual_pool[:extra_needed])

        # VÒNG 1: KHỞI ĐỘNG (Phản xạ trắc nghiệm nhanh)
        r1_questions = []
        for q in conceptual_pool[:cfg_r1.question_count]:
            item = copy.deepcopy(q)
            item.round_number = 1
            item.question_type = "speed_mcq"
            item.time_limit_sec = cfg_r1.time_limit_sec
            item.base_score = 10
            item.allows_star_of_hope = False
            r1_questions.append(item)

        # VÒNG 2: VƯỢT CHƯỚNG NGẠI VẬT (Khái niệm liên kết)
        r2_start = cfg_r1.question_count
        r2_end = r2_start + cfg_r2.question_count
        r2_questions = []
        for q in conceptual_pool[r2_start:r2_end]:
            item = copy.deepcopy(q)
            item.round_number = 2
            item.question_type = "obstacle_clue"
            item.time_limit_sec = cfg_r2.time_limit_sec
            item.base_score = 15
            item.allows_star_of_hope = False
            r2_questions.append(item)

        # VÒNG 3: TĂNG TỐC (Bài toán tính toán mạng đa bước / CIDR / delay)
        r3_questions = []
        for q in calculation_pool[:cfg_r3.question_count]:
            item = copy.deepcopy(q)
            item.round_number = 3
            item.question_type = "multi_hop_scenario"
            item.time_limit_sec = cfg_r3.time_limit_sec
            item.base_score = 20
            item.allows_star_of_hope = False
            item.difficulty = "HARD"
            r3_questions.append(item)

        # VÒNG 4: VỀ ĐÍCH (Chuyên đề nâng cao & Cược Ngôi sao hy vọng)
        r4_start = cfg_r3.question_count
        r4_end = r4_start + cfg_r4.question_count
        r4_questions = []
        for q in calculation_pool[r4_start:r4_end]:
            item = copy.deepcopy(q)
            item.round_number = 4
            item.question_type = "adversarial_essay"
            item.time_limit_sec = cfg_r4.time_limit_sec
            item.base_score = 30
            item.allows_star_of_hope = True
            item.difficulty = "EXTREME"
            r4_questions.append(item)

        rounds = [
            OlympicRoundSet(
                round_number=1,
                round_name="Khởi Động",
                round_theme="Phản xạ tốc độ & Nhận diện khái niệm cốt lõi",
                difficulty=cfg_r1.difficulty,
                time_limit_per_question_sec=cfg_r1.time_limit_sec,
                questions=r1_questions
            ),
            OlympicRoundSet(
                round_number=2,
                round_name="Vượt Chướng Ngại Vật",
                round_theme="Tư duy liên kết & Nhận diện từ khóa chướng ngại",
                difficulty=cfg_r2.difficulty,
                time_limit_per_question_sec=cfg_r2.time_limit_sec,
                obstacle_keyword="INTERNET",
                obstacle_clue_count=len(r2_questions),
                questions=r2_questions
            ),
            OlympicRoundSet(
                round_number=3,
                round_name="Tăng Tốc",
                round_theme="Bài toán tính toán hiệu năng, phân chia subnet & CIDR",
                difficulty=cfg_r3.difficulty,
                time_limit_per_question_sec=cfg_r3.time_limit_sec,
                questions=r3_questions
            ),
            OlympicRoundSet(
                round_number=4,
                round_name="Về Đích",
                round_theme="Chuyên đề phản biện nâng cao & Đặt cược Ngôi sao hy vọng",
                difficulty=cfg_r4.difficulty,
                time_limit_per_question_sec=cfg_r4.time_limit_sec,
                questions=r4_questions
            )
        ]

        return FullOlympicExam(
            document_id=bundle.document_id,
            document_title=bundle.document_title,
            match_mode="ARENA_COMPETITION",
            rounds=rounds,
            total_questions=sum(len(r.questions) for r in rounds)
        )

    @classmethod
    def _build_practice_exam(
        cls, 
        questions: List[OlympicQuestion], 
        bundle: ExtractedKnowledgeBundle, 
        config: UserMatchConfig
    ) -> FullOlympicExam:
        """Xây dựng bộ đề Luyện tập nguyên bản"""
        q_list = copy.deepcopy(questions)

        if config.practice_order == "random":
            random.shuffle(q_list)

        # Lọc theo Vòng nếu người dùng chọn
        if config.practice_filter == "ONLY_ROUND_1":
            q_list = [q for q in q_list if "Calculation" not in q.knowledge_dimension][:50]
        elif config.practice_filter in ["ONLY_ROUND_3", "ONLY_ROUND_4"]:
            q_list = [q for q in q_list if "Calculation" in q.knowledge_dimension][:50]

        chunk_size = 25
        rounds: List[OlympicRoundSet] = []

        if len(q_list) <= chunk_size:
            rounds.append(OlympicRoundSet(
                round_number=1,
                round_name="Luyện Tập Chuyên Sâu",
                round_theme="Chế độ Dojo không áp lực, hỗ trợ xem 2 tầng gợi ý và trích dẫn",
                difficulty="MEDIUM",
                time_limit_per_question_sec=0,
                questions=q_list
            ))
        else:
            for i in range(0, len(q_list), chunk_size):
                sub_q = q_list[i:i+chunk_size]
                r_num = (i // chunk_size) + 1
                rounds.append(OlympicRoundSet(
                    round_number=r_num,
                    round_name=f"Luyện Tập - Chặng {r_num}",
                    round_theme=f"Luyện tập câu {i+1} đến {i+len(sub_q)}",
                    difficulty="MEDIUM",
                    time_limit_per_question_sec=0,
                    questions=sub_q
                ))

        return FullOlympicExam(
            document_id=bundle.document_id,
            document_title=bundle.document_title,
            match_mode="PRACTICE_DOJO",
            rounds=rounds,
            total_questions=sum(len(r.questions) for r in rounds)
        )
