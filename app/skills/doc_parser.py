import re
import uuid
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Set
from pypdf import PdfReader
from docx import Document as DocxDocument

from app.models.schemas_extracted import (
    ChunkMetadata,
    CoreDefinition,
    FormulaOrTheorem,
    CausalRelationship,
    EdgeCase,
    ConceptMap,
    ExtractedKnowledgeBundle,
    BloomLevel,
)

VIETNAMESE_STOPWORDS = {
    "và", "hoặc", "hay", "là", "của", "với", "trong", "cho", "từ", "ở", "tại", "do",
    "bởi", "khi", "nếu", "thì", "được", "bị", "các", "những", "một", "này", "đó",
    "kia", "sự", "việc", "quá trình", "theo", "như", "nhưng", "tuy", "vì", "vậy",
    "để", "nên", "mỗi", "mọi", "cả", "nhiều", "ít", "đang", "đã", "sẽ", "vừa",
    "mới", "cũng", "vẫn", "chỉ", "luôn", "thường", "rất", "quá", "lắm", "hơn",
    "nhất", "không", "chưa", "chẳng", "sau", "trước", "giữa", "dưới", "trên",
    "ngoài", "bên", "qua", "lại", "ra", "vào", "lên", "xuống", "đến", "tới",
    "and", "or", "is", "are", "the", "a", "an", "of", "in", "to", "for", "with",
    "on", "at", "by", "from", "as", "that", "this", "these", "those", "it", "its"
}

def clean_and_validate_term(raw_term: str, original_text: str = "") -> Optional[str]:
    """
    Chuẩn hóa và bảo tồn chính xác thuật ngữ chuyên ngành, từ viết tắt và dạng song ngữ:
    - Loại bỏ triệt để từ nối (và, hoặc, là, của, với...), hư từ tiếng Việt / tiếng Anh.
    - Giữ nguyên casing của từ viết tắt (HTTP, TCP, UDP, LAN, WAN, DSL, HFC, FTTH, CIDR, NAT, IPv4, IPv6...).
    - Giữ nguyên cấu trúc song ngữ: 'Mạng truy cập (Access Networks)'.
    """
    if not raw_term:
        return None

    term = raw_term.strip().strip(":;.,-_–—*\"' \t\n[]{}")
    if not term:
        return None

    # Lọc bỏ tiền tố từ nối/hư từ
    stop_prefixes = [
        "và ", "hoặc ", "hay ", "nhưng ", "do đó ", "vì vậy ", "trong đó ", "ngoài ra ",
        "bởi vì ", "khi ", "nếu ", "thì ", "là ", "của ", "với ", "trong ", "cho ", "tại ",
        "các ", "những ", "một ", "đây là ", "đó là ", "như là ", "được xem là ", "gọi là ",
        "khái niệm ", "thuật ngữ ", "về ", "đối với ", "theo ",
        "and ", "or ", "the ", "a ", "an ", "in ", "with ", "for ", "by ", "is "
    ]
    changed = True
    while changed:
        changed = False
        lower_t = term.lower()
        for p in stop_prefixes:
            if lower_t.startswith(p):
                term = term[len(p):].strip().strip(":;.,-_–—*\"' \t\n[]{}")
                changed = True
                break

    if not term:
        return None

    lower_cleaned = term.lower()
    if lower_cleaned in VIETNAMESE_STOPWORDS:
        return None

    # Lọc bỏ hoàn toàn các tiêu đề cấu trúc như 'Câu 181', 'Phần 1', 'Chương 2'
    if re.match(r'^(câu|phần|chương|bài|mục|đáp án|giải thích)\s*\d*', lower_cleaned):
        return None

    if len(term) < 2 or len(term) > 60:
        return None

    if lower_cleaned in ["điều này", "yếu tố này", "vấn đề này", "khái niệm này", "mục này", "phần này", "hệ thống này"]:
        return None

    # Bảo tồn casing từ văn bản gốc
    if original_text:
        pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        match = pattern.search(original_text)
        if match:
            return match.group(0).strip()

    # Nếu có ký tự in hoa (như TCP, UDP, DSL, IPv6), giữ nguyên
    if any(c.isupper() for c in term[1:]):
        return term

    return term[0].upper() + term[1:]

class KnowledgeGraphExtractor:
    """
    Agent 1: Knowledge_Graph_Extractor
    Xử lý tài liệu, làm sạch, phân đoạn ngữ cảnh (semantic chunking) 
    và trích xuất Bản đồ khái niệm (Concept Map) gắn nhãn phân tầng nhận thức Bloom.
    """

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_file(self, file_path: str) -> Tuple[str, str, List[Tuple[str, str]]]:
        path = Path(file_path)
        ext = path.suffix.lower()
        title = path.stem.replace("_", " ").title()
        sections: List[Tuple[str, str]] = []

        if ext == ".pdf":
            reader = PdfReader(str(path))
            for i, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                cleaned = self._clean_text(txt)
                if cleaned:
                    sections.append((f"Trang {i + 1}", cleaned))
        elif ext == ".docx":
            doc = DocxDocument(str(path))
            current_sec = "Mở đầu"
            sec_buffer = []
            for p in doc.paragraphs:
                txt = p.text.strip()
                if not txt:
                    continue
                if p.style and ("Heading" in p.style.name or "Title" in p.style.name):
                    if sec_buffer:
                        sections.append((current_sec, self._clean_text("\n".join(sec_buffer))))
                        sec_buffer = []
                    current_sec = txt
                else:
                    sec_buffer.append(txt)
            if sec_buffer:
                sections.append((current_sec, self._clean_text("\n".join(sec_buffer))))
        elif ext in [".md", ".txt"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            parts = re.split(r"(?m)^(?=#{1,3}\s+)", content)
            for part in parts:
                clean_part = self._clean_text(part)
                if clean_part:
                    match = re.match(r"^#{1,3}\s+(.*)", part)
                    sec_name = match.group(1).strip() if match else "Nội dung"
                    sections.append((sec_name, clean_part))
        else:
            raise ValueError(f"Định dạng file không hỗ trợ: {ext}")

        full_text = "\n\n".join([text for _, text in sections])
        return title, full_text, sections

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def semantic_chunking(self, sections: List[Tuple[str, str]]) -> List[ChunkMetadata]:
        chunks: List[ChunkMetadata] = []
        chunk_idx = 1

        for sec_name, text in sections:
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            current_chunk = []
            current_len = 0

            for p in paragraphs:
                p_len = len(p)
                if current_len + p_len > self.chunk_size and current_chunk:
                    chunk_text = " ".join(current_chunk)
                    bloom = self._infer_chunk_bloom(chunk_text)
                    chunks.append(
                        ChunkMetadata(
                            chunk_id=f"CHK_{chunk_idx:03d}",
                            content=chunk_text,
                            page_or_section=sec_name,
                            token_count_approx=len(chunk_text.split()),
                            primary_bloom_level=bloom,
                        )
                    )
                    chunk_idx += 1
                    overlap_tokens = chunk_text.split()[-int(self.chunk_overlap / 5):]
                    current_chunk = [" ".join(overlap_tokens), p]
                    current_len = len(current_chunk[0]) + p_len
                else:
                    current_chunk.append(p)
                    current_len += p_len

            if current_chunk:
                chunk_text = " ".join(current_chunk)
                bloom = self._infer_chunk_bloom(chunk_text)
                chunks.append(
                    ChunkMetadata(
                        chunk_id=f"CHK_{chunk_idx:03d}",
                        content=chunk_text,
                        page_or_section=sec_name,
                        token_count_approx=len(chunk_text.split()),
                        primary_bloom_level=bloom,
                    )
                )
                chunk_idx += 1

        return chunks

    def _infer_chunk_bloom(self, text: str) -> BloomLevel:
        t = text.lower()
        if any(w in t for w in ["tuy nhiên", "ngoại trừ", "rủi ro", "giới hạn", "ngược lại", "phá vỡ"]):
            return "ANALYZE_EVALUATE"
        if any(w in t for w in ["khi", "nếu", "dẫn đến", "công thức", "tính toán", "áp dụng"]):
            return "APPLY"
        if any(w in t for w in ["giải thích", "nguyên lý", "bởi vì", "cơ chế"]):
            return "UNDERSTAND"
        return "REMEMBER"

    def extract_concept_map(self, chunks: List[ChunkMetadata], doc_title: str) -> ConceptMap:
        core_defs: List[CoreDefinition] = []
        formulas: List[FormulaOrTheorem] = []
        causals: List[CausalRelationship] = []
        edge_cases: List[EdgeCase] = []
        domain_terms_set = set()

        def_patterns = [
            # 1. Dạng có từ khóa định nghĩa chuẩn xác (ưu tiên)
            r"([A-ZÀ-Ỹa-zà-ỹ0-9\s_\-/(/)]+?)\s+(?:được định nghĩa là|chính là|đề cập đến|nghĩa là|is defined as|refers to)\s+([^.,;\n]{15,180})",
            # 2. Dạng Khái niệm / Thuật ngữ / In đậm
            r"(?:Khái niệm|Thuật ngữ)\s+([A-ZÀ-Ỹa-zà-ỹ0-9\s_\-/(/)]+?)\s*:\s*([^.,;\n]{15,180})",
            r"\*\*([A-ZÀ-Ỹa-zà-ỹ0-9\s_\-/(/)]+?)\*\*\s*:\s*([^.,;\n]{15,180})",
            # 3. Dạng song ngữ: Mạng truy cập (Access Networks) là...
            r"([A-ZÀ-Ỹa-zà-ỹ0-9\s_\-]+\s*\([A-Za-z0-9\s/_\-]+\))\s+là\s+([^.,;\n]{15,180})",
            # 4. Dạng từ viết tắt kỹ thuật: HTTP là..., TCP là...
            r"\b([A-Z0-9]{2,8}(?:/[A-Z0-9]+)?)\s+là\s+([^.,;\n]{15,180})",
            # 5. Dạng chung '... là ...'
            r"([A-ZÀ-Ỹa-zà-ỹ0-9\s_\-/(/)]+?)\s+là\s+([^.,;\n]{15,180})",
        ]

        formula_patterns = [
            r"(?:Định lý|Nguyên lý|Quy tắc|Định luật|Công thức|Theorem|Principle|Law)\s+([A-ZÀ-Ỹa-zà-ỹ0-9\s_-]{3,40})\s*[:\-–]?\s*([^.\n]{20,200})",
            r"([A-ZÀ-Ỹa-zà-ỹ0-9\s_-]{3,30})\s+(?:tuân theo nguyên lý|được biểu diễn bằng công thức|khẳng định rằng)\s+([^.\n]{20,200})",
        ]

        causal_patterns = [
            r"(?:Khi|Nếu|Do|Bởi vì)\s+([^,]{10,80}),\s*(?:thì|dẫn đến|gây ra|làm cho|khiến cho)\s+([^.\n]{10,120})",
            r"([^.]{10,80})\s+(?:dẫn tới|gây ra|tác động làm|kéo theo|dẫn đến kết quả)\s+([^.\n]{10,100})",
        ]

        edge_patterns = [
            r"(?:Tuy nhiên|Ngoại trừ|Trừ trường hợp|Điểm hạn chế là|Trong điều kiện biên|Tuy thế|Chỉ áp dụng khi)\s*[,:]?\s*([^.\n]{20,180})",
            r"([^.]{15,100})\s+(?:sẽ thất bại nếu|không hoạt động khi|không còn đúng trong trường hợp)\s+([^.\n]{10,100})",
        ]

        for chk in chunks:
            text = chk.content

            # Bóc tách ngân hàng thuật ngữ chuyên môn từ chunk
            # a. Từ viết tắt kỹ thuật (HTTP, TCP, UDP, LAN, WAN, DSL, HFC, FTTH, CIDR, NAT, IPv4, IPv6...)
            for acronym in re.findall(r"\b[A-Z0-9]{2,8}(?:/[A-Z0-9]+)?\b", text):
                if acronym.lower() not in VIETNAMESE_STOPWORDS and not acronym.isnumeric():
                    domain_terms_set.add(acronym)

            # b. Thuật ngữ in đậm
            for b_term in re.findall(r"\*\*([^*]{2,40})\*\*", text):
                cleaned_b = clean_and_validate_term(b_term, text)
                if cleaned_b:
                    domain_terms_set.add(cleaned_b)

            # c. Thuật ngữ song ngữ (VD: Mạng truy cập (Access Networks))
            for biling in re.findall(r"\b([A-ZÀ-Ỹa-zà-ỹ0-9\s_-]{2,30}\s*\([A-Za-z0-9\s/_\-]+\))", text):
                cleaned_bi = clean_and_validate_term(biling, text)
                if cleaned_bi:
                    domain_terms_set.add(cleaned_bi)

            # 1. Định nghĩa (Bloom: REMEMBER)
            for pat in def_patterns:
                matches = re.finditer(pat, text, re.IGNORECASE)
                for m in matches:
                    raw_term = m.group(1).strip()
                    definition = m.group(2).strip()
                    term = clean_and_validate_term(raw_term, text)
                    if not term:
                        continue
                    if len(term.split()) > 7 or len(definition) < 15:
                        continue

                    domain_terms_set.add(term)
                    core_defs.append(
                        CoreDefinition(
                            term=term,
                            definition=definition,
                            chunk_id=chk.chunk_id,
                            exact_quote=m.group(0).strip(),
                            importance_level="high",
                            bloom_level="REMEMBER",
                        )
                    )

            # 2. Định lý / Công thức (Bloom: APPLY)
            for pat in formula_patterns:
                matches = re.finditer(pat, text, re.IGNORECASE)
                for m in matches:
                    raw_name = m.group(1).strip()
                    name = clean_and_validate_term(raw_name, text) or raw_name.strip()
                    statement = m.group(2).strip()
                    formula_name = f"Nguyên lý {name}" if not name.lower().startswith("nguyên lý") else name
                    domain_terms_set.add(name)
                    formulas.append(
                        FormulaOrTheorem(
                            name=formula_name,
                            statement=statement,
                            conditions="Theo ngữ cảnh tài liệu quy định",
                            chunk_id=chk.chunk_id,
                            exact_quote=m.group(0).strip(),
                            bloom_level="APPLY",
                        )
                    )

            # 3. Nhân - Quả (Bloom: APPLY)
            for pat in causal_patterns:
                matches = re.finditer(pat, text, re.IGNORECASE)
                for m in matches:
                    cause = m.group(1).strip()
                    effect = m.group(2).strip()
                    causals.append(
                        CausalRelationship(
                            cause=cause,
                            effect=effect,
                            mechanism="Liên kết nhân quả trực tiếp",
                            chunk_id=chk.chunk_id,
                            exact_quote=m.group(0).strip(),
                            bloom_level="APPLY",
                        )
                    )

            # 4. Ngoại lệ / Biên (Bloom: ANALYZE_EVALUATE)
            for pat in edge_patterns:
                matches = re.finditer(pat, text, re.IGNORECASE)
                for m in matches:
                    matched_str = m.group(1).strip() if m.lastindex >= 1 else m.group(0).strip()
                    edge_cases.append(
                        EdgeCase(
                            scenario="Tình huống ngoại lệ đặc biệt",
                            consequence=matched_str,
                            exception_rule="Cần xử lý rào chắn hoặc xem xét điều kiện ràng buộc",
                            chunk_id=chk.chunk_id,
                            exact_quote=m.group(0).strip(),
                            bloom_level="ANALYZE_EVALUATE",
                        )
                    )

        # Fallback an toàn: nếu thiếu định nghĩa, quét các thuật ngữ in đậm hoặc từ viết tắt trong tài liệu
        if len(core_defs) < 3 and chunks:
            for chk in chunks[:4]:
                sentences = [s.strip() for s in re.split(r"[.!?]", chk.content) if len(s.strip()) > 30]
                for s in sentences:
                    # Tìm thuật ngữ in đậm hoặc từ viết tắt trong câu này
                    found_terms = re.findall(r"\*\*([^*]{2,40})\*\*", s) or re.findall(r"\b[A-Z0-9]{2,8}(?:/[A-Z0-9]+)?\b", s)
                    for ft in found_terms:
                        cleaned_ft = clean_and_validate_term(ft, s)
                        if cleaned_ft and cleaned_ft.lower() not in [d.term.lower() for d in core_defs]:
                            core_defs.append(
                                CoreDefinition(
                                    term=cleaned_ft,
                                    definition=s,
                                    chunk_id=chk.chunk_id,
                                    exact_quote=s,
                                    importance_level="medium",
                                    bloom_level="REMEMBER",
                                )
                            )
                            domain_terms_set.add(cleaned_ft)
                            break
                    if len(core_defs) >= 6:
                        break

        if not edge_cases and chunks:
            edge_cases.append(
                EdgeCase(
                    scenario="Điều kiện biên hệ thống",
                    consequence="Tài liệu yêu cầu tuân thủ đúng các thông số và ngữ cảnh vận hành.",
                    exception_rule="Kiểm tra tính toàn vẹn dữ liệu và độ trễ.",
                    chunk_id=chunks[0].chunk_id,
                    exact_quote=chunks[0].content[:150],
                    bloom_level="ANALYZE_EVALUATE",
                )
            )

        unique_defs = {d.term.lower(): d for d in core_defs if d.term.lower() not in VIETNAMESE_STOPWORDS}
        for d in unique_defs.values():
            domain_terms_set.add(d.term)

        # Danh mục thuật ngữ chuyên ngành đã làm sạch
        glossary_list = [
            t for t in sorted(domain_terms_set, key=lambda x: (len(x), x))
            if t.lower() not in VIETNAMESE_STOPWORDS and len(t) >= 2
        ]

        return ConceptMap(
            core_definitions=list(unique_defs.values())[:15],
            formulas_and_theorems=formulas[:10],
            causal_relationships=causals[:10],
            edge_cases=edge_cases[:8],
            domain_glossary=glossary_list,
        )

    def process_document(self, file_path: str, doc_id: str = None) -> ExtractedKnowledgeBundle:
        doc_id = doc_id or f"DOC_{uuid.uuid4().hex[:8]}"

        # TỰ ĐỘNG PHÁT HIỆN & KHÓA LUỒNG CHO BỘ ĐỀ TRẮC NGHIỆM MARKDOWN NGUYÊN BẢN
        ext = Path(file_path).suffix.lower()
        if ext in [".md", ".txt"]:
            try:
                content = Path(file_path).read_text(encoding="utf-8")
                from app.services.md_quiz_parser import DirectMDQuizParser
                if DirectMDQuizParser.is_markdown_quiz(content):
                    return DirectMDQuizParser.build_knowledge_bundle(
                        content=content,
                        doc_id=doc_id,
                        doc_title=Path(file_path).name
                    )
            except Exception:
                pass

        title, _, sections = self.parse_file(file_path)
        chunks = self.semantic_chunking(sections)
        concept_map = self.extract_concept_map(chunks, title)

        topics = list(set([sec for sec, _ in sections if sec != "Nội dung"]))[:5]
        if not topics:
            topics = [title]

        return ExtractedKnowledgeBundle(
            document_id=doc_id,
            document_title=title,
            total_chunks=len(chunks),
            detected_topics=topics,
            chunks=chunks,
            concept_map=concept_map,
        )

# Tương thích ngược
DocumentParserAndExtractor = KnowledgeGraphExtractor
