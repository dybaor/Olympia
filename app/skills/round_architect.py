import random
import uuid
from typing import List, Optional, Dict
from app.models.schemas_extracted import ExtractedKnowledgeBundle, CoreDefinition, FormulaOrTheorem, CausalRelationship, EdgeCase
from app.models.schemas_olympic import (
    OlympicQuestion,
    OlympicRoundSet,
    FullOlympicExam,
    SourceCitation,
    ProgressiveHints,
    RoundConfig,
    UserMatchConfig,
    DifficultyLevel,
    BloomLevel,
)

class DynamicOlympicArchitect:
    """
    Agent 2: Dynamic_Olympic_Architect (Kiến trúc sư đề thi tham số hóa)
    Thiết kế đề thi Olympic 4 vòng dựa trên cấu hình tùy biến của người dùng:
    - Độ khó tham số hóa: EASY | MEDIUM | HARD | EXTREME
    - Giới hạn thời gian tùy chỉnh cho từng vòng
    - Luôn sinh kèm 2 tầng gợi ý (progressive_hints) và giải thích từng bước (step_by_step_explanation)
    - Hỗ trợ tạo biến thể câu hỏi (generate_question_variant) phục vụ luyện tập.
    """

    def __init__(self, bundle: ExtractedKnowledgeBundle):
        self.bundle = bundle
        self.cmap = bundle.concept_map
        self.chunks_dict = {c.chunk_id: c for c in bundle.chunks}

    def generate_round_1_khoi_dong(self, config: RoundConfig = None) -> OlympicRoundSet:
        cfg = config or RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=8)
        count = cfg.question_count
        diff = cfg.difficulty
        time_sec = cfg.time_limit_sec

        questions: List[OlympicQuestion] = []
        defs = list(self.cmap.core_definitions)
        random.shuffle(defs)

        all_terms = [d.term for d in defs]
        if len(all_terms) < 4:
            all_terms.extend(["Độ phức tạp thuật toán", "Tính toàn vẹn dữ liệu", "Bất biến hệ thống", "Mô hình xác thực"])

        for i, item in enumerate(defs[:count]):
            other_terms = [t for t in all_terms if t.lower() != item.term.lower()]
            distractors = random.sample(other_terms, min(3, len(other_terms)))
            while len(distractors) < 3:
                distractors.append(f"Khái niệm phụ {len(distractors) + 1}")

            options = [item.term] + distractors
            random.shuffle(options)

            q_id = f"R1_Q{i+1:02d}"
            
            # Điều chỉnh độ khó prompt theo difficulty
            if diff == "EASY":
                prompt = f"Thuật ngữ nào sau đây được định nghĩa là: \"{item.definition}\"?"
                hint1 = f"Đây là một khái niệm cơ bản liên quan đến mục '{self.chunks_dict.get(item.chunk_id, None).page_or_section if self.chunks_dict.get(item.chunk_id) else 'nền tảng'}'."
                hint2 = f"Tên thuật ngữ này bắt đầu bằng chữ '{item.term[0]}'."
            elif diff == "HARD":
                prompt = f"[Khái niệm trọng tâm] Nhận diện thuật ngữ đặc thù mô tả chính xác nội dung: \"{item.definition}\" (lưu ý loại trừ các thuật ngữ tương tự trong cùng ngữ cảnh)."
                hint1 = "Tập trung vào đặc tính cốt lõi của định nghĩa được nêu trong câu hỏi."
                hint2 = f"Đáp án không phải là '{distractors[0]}' mà liên quan trực tiếp đến {item.term}."
            elif diff == "EXTREME":
                prompt = f"[Phản xạ cấp cao] Trong lý thuyết đã học, cấu trúc nào định hình trực tiếp cơ chế: \"{item.definition}\"?"
                hint1 = "Phân biệt giữa hiện tượng bề mặt và thuật ngữ chuyên ngành định danh."
                hint2 = f"Thuật ngữ có {len(item.term.split())} từ."
            else: # MEDIUM
                prompt = f"Thuật ngữ nào sau đây được định nghĩa là: \"{item.definition}\"?"
                hint1 = "Hãy nhớ lại các định nghĩa nền tảng được giới thiệu ở phần đầu tài liệu."
                hint2 = f"Thuật ngữ này đối chiếu trực tiếp với: \"{item.exact_quote[:50]}...\""

            chunk_meta = self.chunks_dict.get(item.chunk_id)
            sec_name = chunk_meta.page_or_section if chunk_meta else "Tài liệu gốc"

            steps = [
                f"Bước 1: Đọc kỹ định nghĩa: '{item.definition}'.",
                f"Bước 2: So sánh đặc điểm với các lựa chọn: loại trừ {', '.join(distractors[:2])}.",
                f"Bước 3: Khẳng định thuật ngữ chính xác là '{item.term}' dựa trên trích dẫn: '{item.exact_quote}'."
            ]

            questions.append(
                OlympicQuestion(
                    question_id=q_id,
                    round_number=1,
                    question_type="speed_mcq",
                    bloom_level="REMEMBER",
                    difficulty=diff,
                    prompt=prompt,
                    options=options,
                    correct_answer=item.term,
                    explanation=f"Đáp án chính xác là **{item.term}**.\nTheo tài liệu trích dẫn: \"{item.exact_quote}\".",
                    step_by_step_explanation=steps,
                    progressive_hints=ProgressiveHints(
                        level_1_hint=hint1,
                        level_2_hint=hint2,
                    ),
                    source_citation=SourceCitation(
                        chunk_id=item.chunk_id,
                        exact_quote=item.exact_quote,
                        page_or_section=sec_name,
                    ),
                    time_limit_sec=time_sec,
                    base_score=10,
                    allows_star_of_hope=False,
                    knowledge_dimension="Concept",
                )
            )

        return OlympicRoundSet(
            round_number=1,
            round_name="Khởi động",
            round_theme="Tốc độ & Nhận diện Khái niệm Cốt lõi",
            difficulty=diff,
            time_limit_per_question_sec=time_sec,
            questions=questions,
        )

    def generate_round_2_vuot_chuong_ngai_vat(self, config: RoundConfig = None) -> OlympicRoundSet:
        cfg = config or RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=4)
        count = cfg.question_count
        diff = cfg.difficulty
        time_sec = cfg.time_limit_sec

        candidate_keywords = []
        if self.bundle.detected_topics:
            candidate_keywords.extend([t.upper().replace(" ", "") for t in self.bundle.detected_topics if 4 <= len(t.replace(" ", "")) <= 20])
        if self.cmap.core_definitions:
            candidate_keywords.extend([d.term.upper().replace(" ", "") for d in self.cmap.core_definitions if 4 <= len(d.term.replace(" ", "")) <= 20])

        obstacle_keyword = candidate_keywords[0] if candidate_keywords else "DONG THUAN"
        obstacle_keyword = "".join(ch for ch in obstacle_keyword if ch.isalnum() or ch == " ")

        questions: List[OlympicQuestion] = []
        clue_pool = []
        for d in self.cmap.core_definitions:
            clue_pool.append((d.term, d.definition, d.chunk_id, d.exact_quote, "Concept", "REMEMBER"))
        for f in self.cmap.formulas_and_theorems:
            clue_pool.append((f.name, f.statement, f.chunk_id, f.exact_quote, "Formula", "UNDERSTAND"))
        for c in self.cmap.causal_relationships:
            clue_pool.append((c.cause, f"Nguyên nhân kích hoạt hệ quả '{c.effect}'", c.chunk_id, c.exact_quote, "Causality", "APPLY"))

        random.shuffle(clue_pool)
        selected_clues = clue_pool[:count]

        while len(selected_clues) < count:
            chk = self.bundle.chunks[0] if self.bundle.chunks else None
            cid = chk.chunk_id if chk else "CHK_001"
            txt = chk.content[:100] if chk else "Hệ thống chuẩn tắc"
            selected_clues.append((
                "TỐC ĐỘ",
                "Yếu tố quyết định ưu thế xử lý trong các hệ thống hiện đại",
                cid,
                txt,
                "Concept",
                "REMEMBER"
            ))

        for idx, (answer, prompt_hint, chunk_id, quote, dim, b_level) in enumerate(selected_clues[:count]):
            q_id = f"R2_CLUE_{idx+1}"
            prompt = f"[Hàng ngang {idx+1} ({len(answer.replace(' ', ''))} chữ cái)]: {prompt_hint}?"

            chunk_meta = self.chunks_dict.get(chunk_id)
            sec_name = chunk_meta.page_or_section if chunk_meta else "Tài liệu gốc"

            options = [answer]
            for other in clue_pool:
                if other[0] != answer and len(options) < 4:
                    options.append(other[0])
            while len(options) < 4:
                options.append(f"Gợi ý phụ {len(options)}")
            random.shuffle(options)

            steps = [
                f"Bước 1: Phân tích số lượng ký tự ({len(answer.replace(' ', ''))} chữ cái).",
                f"Bước 2: Đối chiếu ngữ cảnh tài liệu: '{prompt_hint}'.",
                f"Bước 3: Xác định từ khóa hàng ngang là '{answer}', góp phần lật mở chướng ngại vật '{obstacle_keyword}'."
            ]

            questions.append(
                OlympicQuestion(
                    question_id=q_id,
                    round_number=2,
                    question_type="obstacle_clue",
                    bloom_level=b_level,
                    difficulty=diff,
                    prompt=prompt,
                    options=options,
                    correct_answer=answer,
                    acceptable_keywords=[answer.lower(), answer.replace(" ", "").lower()],
                    explanation=f"Từ khóa hàng ngang là **{answer}**, trích xuất từ: \"{quote}\"",
                    step_by_step_explanation=steps,
                    progressive_hints=ProgressiveHints(
                        level_1_hint=f"Hàng ngang này có độ dài {len(answer.replace(' ', ''))} ký tự.",
                        level_2_hint=f"Chữ cái đầu tiên là '{answer[0]}'. Liên quan đến mục {sec_name}.",
                    ),
                    source_citation=SourceCitation(
                        chunk_id=chunk_id,
                        exact_quote=quote,
                        page_or_section=sec_name,
                    ),
                    time_limit_sec=time_sec,
                    base_score=10,
                    allows_star_of_hope=False,
                    knowledge_dimension=dim,
                )
            )

        return OlympicRoundSet(
            round_number=2,
            round_name="Vượt chướng ngại vật",
            round_theme="Tư duy Liên kết & Giải mã Ẩn số Trung tâm",
            difficulty=diff,
            time_limit_per_question_sec=time_sec,
            obstacle_keyword=obstacle_keyword,
            obstacle_clue_count=len(questions),
            questions=questions,
        )

    def generate_round_3_tang_toc(self, config: RoundConfig = None) -> OlympicRoundSet:
        cfg = config or RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=30, question_count=4)
        count = cfg.question_count
        diff = cfg.difficulty
        time_sec = cfg.time_limit_sec

        questions: List[OlympicQuestion] = []
        causals = self.cmap.causal_relationships
        formulas = self.cmap.formulas_and_theorems

        scenarios = []
        if causals and formulas:
            for c, f in zip(causals[:count], formulas[:count]):
                scenarios.append((
                    f"Giả sử trong một hệ thống thực nghiệm, người ta phát hiện hiện tượng '{c.cause}'. "
                    f"Dựa trên nguyên lý '{f.name}' ({f.statement}), điều gì sẽ xảy ra và cơ chế tác động nào được kích hoạt?",
                    f"Kích hoạt '{c.effect}' thông qua {c.mechanism}.",
                    [
                        f"Kích hoạt '{c.effect}' thông qua {c.mechanism}.",
                        f"Không gây tác động nào do {f.name} tự động triệt tiêu sai số.",
                        f"Đảo ngược toàn bộ quy trình mà không theo cơ chế {c.mechanism}.",
                        f"Gây sập toàn bộ hệ thống ngay lập tức mà không có hệ quả {c.effect}."
                    ],
                    f.chunk_id,
                    f.exact_quote,
                    "MultiHop",
                    f"Xem xét tác động kép của {f.name} khi xuất hiện {c.cause}",
                    f"Cơ chế mấu chốt là '{c.mechanism}', dẫn tới '{c.effect}'"
                ))

        for c in causals[len(scenarios):count]:
            scenarios.append((
                f"Tình huống thực tế: Kỹ sư ghi nhận điều kiện đầu vào '{c.cause}'. "
                f"Hãy phân tích chuỗi suy luận logic: Hiện tượng này sẽ kích hoạt phản ứng dây chuyền nào?",
                f"Dẫn đến '{c.effect}' theo cơ chế {c.mechanism}.",
                [
                    f"Dẫn đến '{c.effect}' theo cơ chế {c.mechanism}.",
                    f"Ngăn chặn hoàn toàn hiện tượng '{c.effect}' diễn ra.",
                    f"Bỏ qua cơ chế {c.mechanism} và tạo ra trạng thái cân bằng ngẫu nhiên.",
                    f"Hệ thống tự động vô hiệu hóa mà không tạo ra bất kỳ tác động nào."
                ],
                c.chunk_id,
                c.exact_quote,
                "Causality",
                "Tìm mối liên kết trực tiếp giữa tiền đề và hệ quả trong tài liệu",
                f"Chú ý cụm từ chỉ cơ chế: '{c.mechanism}'"
            ))

        while len(scenarios) < count:
            chk = self.bundle.chunks[min(len(scenarios), len(self.bundle.chunks)-1)]
            scenarios.append((
                f"Phân tích hệ thống: Khi triển khai giải pháp dựa trên nội dung mục '{chk.page_or_section}', "
                f"yếu tố nào cần được ưu tiên kiểm soát để duy trì tính đúng đắn?",
                f"Tuân thủ chính xác các điều kiện vận hành tại {chk.page_or_section}.",
                [
                    f"Tuân thủ chính xác các điều kiện vận hành tại {chk.page_or_section}.",
                    "Bỏ qua kiểm tra ràng buộc để tối đa hóa tốc độ xử lý.",
                    "Giả định tất cả biến số môi trường luôn ở giá trị lý tưởng.",
                    "Tách biệt hoàn toàn khỏi kiến trúc đã được đặc tả trong tài liệu."
                ],
                chk.chunk_id,
                chk.content[:160],
                "Synthesis",
                f"Đọc lại các yêu cầu vận hành tại mục {chk.page_or_section}",
                "Giải pháp bắt buộc phải tôn trọng ràng buộc kiến trúc thay vì giả định lý tưởng"
            ))

        for idx, (prompt, correct, options, chunk_id, quote, dim, h1, h2) in enumerate(scenarios[:count]):
            q_id = f"R3_Q{idx+1}"
            random.shuffle(options)
            chunk_meta = self.chunks_dict.get(chunk_id)
            sec_name = chunk_meta.page_or_section if chunk_meta else "Tài liệu gốc"

            steps = [
                "Bước 1: Xác định tiền đề và biến số đầu vào của tình huống.",
                f"Bước 2: Áp dụng suy luận đa bước: đối chiếu cơ chế quy định tại {sec_name}.",
                f"Bước 3: Rút ra kết luận duy nhất hợp lý: {correct}."
            ]

            questions.append(
                OlympicQuestion(
                    question_id=q_id,
                    round_number=3,
                    question_type="multi_hop_scenario",
                    bloom_level="APPLY",
                    difficulty=diff,
                    prompt=prompt,
                    options=options,
                    correct_answer=correct,
                    explanation=f"Phân tích logic đa bước:\n{quote}",
                    step_by_step_explanation=steps,
                    progressive_hints=ProgressiveHints(
                        level_1_hint=h1,
                        level_2_hint=h2,
                    ),
                    source_citation=SourceCitation(
                        chunk_id=chunk_id,
                        exact_quote=quote,
                        page_or_section=sec_name,
                    ),
                    time_limit_sec=time_sec,
                    base_score=30,
                    allows_star_of_hope=False,
                    knowledge_dimension=dim,
                )
            )

        return OlympicRoundSet(
            round_number=3,
            round_name="Tăng tốc",
            round_theme="Phân tích Tình huống & Suy luận Đa bước (Multi-hop)",
            difficulty=diff,
            time_limit_per_question_sec=time_sec,
            questions=questions,
        )

    def generate_round_4_ve_dich(self, config: RoundConfig = None) -> OlympicRoundSet:
        cfg = config or RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=45, question_count=3)
        count = cfg.question_count
        diff = cfg.difficulty
        time_sec = cfg.time_limit_sec

        questions: List[OlympicQuestion] = []
        edges = self.cmap.edge_cases

        trap_questions = []
        for edge in edges:
            prompt = (
                f"[Phản biện & Điều kiện biên] Có nhận định cho rằng: 'Quy tắc này luôn đúng trong mọi hoàn cảnh'. "
                f"Dựa trên tài liệu gốc, phản bác hoặc chỉ ra trường hợp ngoại lệ mà nhận định trên bị phá vỡ?"
            )
            correct_ans = f"Nhận định trên sai khi gặp tình huống: {edge.consequence} ({edge.exception_rule})"
            options = [
                correct_ans,
                "Nhận định trên hoàn toàn chính xác, không có bất kỳ ngoại lệ nào tồn tại.",
                "Ngoại lệ chỉ xuất hiện khi có sự can thiệp thủ công từ bên ngoài.",
                "Hệ thống sẽ tự sửa đổi quy tắc mà không bị ảnh hưởng bởi điều kiện biên."
            ]
            trap_questions.append((
                prompt,
                correct_ans,
                options,
                edge.chunk_id,
                edge.exact_quote,
                "EdgeCase",
                "Chú ý các từ khóa loại trừ như 'Tuy nhiên', 'Ngoại trừ', 'Không áp dụng khi'",
                f"Ngoại lệ cụ thể liên quan tới: {edge.consequence[:60]}..."
            ))

        while len(trap_questions) < count:
            chk = self.bundle.chunks[-1] if self.bundle.chunks else None
            cid = chk.chunk_id if chk else "CHK_001"
            qtext = chk.content[:160] if chk else "Tài liệu quy định ranh giới chặt chẽ."
            prompt = (
                f"[Phản biện giả định] Nếu một giả thuyết đi ngược lại kết luận tại mục '{chk.page_or_section if chk else 'Tổng kết'}', "
                f"luận điểm cốt lõi nào trong tài liệu dùng để bác bỏ giả thuyết sai lệch đó?"
            )
            correct_ans = f"Dựa vào nguyên lý nền tảng: {qtext}"
            options = [
                correct_ans,
                "Bác bỏ bằng cách chấp nhận cả hai kết quả trái ngược.",
                "Không thể bác bỏ vì tài liệu không đưa ra bất kỳ căn cứ thực nghiệm nào.",
                "Tự động công nhận giả thuyết mới mà không cần đối chiếu."
            ]
            trap_questions.append((
                prompt,
                correct_ans,
                options,
                cid,
                qtext,
                "Synthesis",
                "Tìm nguyên lý nền tảng đóng vai trò bất biến trong tài liệu",
                f"Đối chiếu với nội dung tại '{chk.page_or_section if chk else 'Phần cuối'}'"
            ))

        for idx, (prompt, correct, options, chunk_id, quote, dim, h1, h2) in enumerate(trap_questions[:count]):
            q_id = f"R4_Q{idx+1}"
            random.shuffle(options)
            chunk_meta = self.chunks_dict.get(chunk_id)
            sec_name = chunk_meta.page_or_section if chunk_meta else "Tài liệu gốc"

            steps = [
                "Bước 1: Bóc tách giả thiết đối kháng (adversarial premise).",
                f"Bước 2: Tìm kiếm điều kiện biên (Edge Case) tại {sec_name}.",
                f"Bước 3: Phản biện và chứng minh trường hợp ngoại lệ: {correct}."
            ]

            questions.append(
                OlympicQuestion(
                    question_id=q_id,
                    round_number=4,
                    question_type="adversarial_essay",
                    bloom_level="ANALYZE_EVALUATE",
                    difficulty=diff,
                    prompt=prompt,
                    options=options,
                    correct_answer=correct,
                    explanation=f"Lời giải phản biện chi tiết: Theo trích dẫn: \"{quote}\"",
                    step_by_step_explanation=steps,
                    progressive_hints=ProgressiveHints(
                        level_1_hint=h1,
                        level_2_hint=h2,
                    ),
                    source_citation=SourceCitation(
                        chunk_id=chunk_id,
                        exact_quote=quote,
                        page_or_section=sec_name,
                    ),
                    time_limit_sec=time_sec,
                    base_score=30,
                    allows_star_of_hope=True,
                    knowledge_dimension=dim,
                )
            )

        return OlympicRoundSet(
            round_number=4,
            round_name="Về đích",
            round_theme="Phản biện, Bẫy Logic, Điều kiện Biên & Ngôi Sao Hy Vọng",
            difficulty=diff,
            time_limit_per_question_sec=time_sec,
            questions=questions,
        )

    def generate_full_olympic_exam(self, match_config: UserMatchConfig = None) -> FullOlympicExam:
        cfg = match_config or UserMatchConfig()
        cfg_map: Dict[int, RoundConfig] = {rc.round_number: rc for rc in cfg.round_configs}

        r1 = self.generate_round_1_khoi_dong(cfg_map.get(1))
        r2 = self.generate_round_2_vuot_chuong_ngai_vat(cfg_map.get(2))
        r3 = self.generate_round_3_tang_toc(cfg_map.get(3))
        r4 = self.generate_round_4_ve_dich(cfg_map.get(4))

        rounds = [r1, r2, r3, r4]
        total_q = sum(len(r.questions) for r in rounds)

        return FullOlympicExam(
            document_id=self.bundle.document_id,
            document_title=self.bundle.document_title,
            match_mode=cfg.match_mode,
            rounds=rounds,
            total_questions=total_q,
        )

    def generate_question_variant(self, original_q: OlympicQuestion) -> OlympicQuestion:
        """
        Tạo biến thể câu hỏi tương tự (Variant) phục vụ chế độ Luyện tập khi người dùng làm sai.
        """
        variant = original_q.model_copy(deep=True)
        variant.question_id = f"{original_q.question_id}_VAR_{random.randint(10, 99)}"
        
        # Đổi cấu trúc câu prompt nhẹ nhàng
        if "được định nghĩa là" in variant.prompt:
            variant.prompt = variant.prompt.replace("được định nghĩa là:", "đề cập đến nội hàm cốt lõi nào sau đây:")
        elif "Khái niệm trọng tâm" in variant.prompt:
            variant.prompt = f"[Câu hỏi rèn luyện] Hãy xác định chính xác thuật ngữ tương ứng với: {variant.prompt.split(':')[-1]}"
        else:
            variant.prompt = f"[Biến thể luyện tập] {variant.prompt}"

        # Xáo trộn lại options
        if variant.options:
            opts = list(variant.options)
            random.shuffle(opts)
            variant.options = opts

        return variant

# Tương thích ngược
OlympicRoundArchitect = DynamicOlympicArchitect
