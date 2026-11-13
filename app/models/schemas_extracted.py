from typing import List, Optional, Literal
from pydantic import BaseModel, Field

BloomLevel = Literal["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE_EVALUATE"]

class ChunkMetadata(BaseModel):
    chunk_id: str
    content: str
    page_or_section: str
    token_count_approx: int = 0
    primary_bloom_level: BloomLevel = "UNDERSTAND"

class CoreDefinition(BaseModel):
    term: str = Field(..., description="Thuật ngữ hoặc khái niệm chính")
    definition: str = Field(..., description="Định nghĩa chuẩn xác theo tài liệu")
    chunk_id: str = Field(..., description="ID của đoạn chứa định nghĩa")
    exact_quote: str = Field(..., description="Trích dẫn nguyên văn từ tài liệu gốc")
    importance_level: str = Field(default="high", description="Mức độ quan trọng: high/medium")
    bloom_level: BloomLevel = "REMEMBER"

class FormulaOrTheorem(BaseModel):
    name: str = Field(..., description="Tên định lý, công thức hoặc quy tắc toán/logic")
    statement: str = Field(..., description="Phát biểu hoặc biểu thức toán học")
    conditions: str = Field(..., description="Điều kiện áp dụng hoặc giả thiết")
    chunk_id: str
    exact_quote: str
    bloom_level: BloomLevel = "APPLY"

class CausalRelationship(BaseModel):
    cause: str = Field(..., description="Nguyên nhân hoặc yếu tố kích hoạt")
    effect: str = Field(..., description="Hệ quả hoặc kết quả sinh ra")
    mechanism: str = Field(..., description="Cơ chế hoặc lý giải liên kết")
    chunk_id: str
    exact_quote: str
    bloom_level: BloomLevel = "APPLY"

class EdgeCase(BaseModel):
    scenario: str = Field(..., description="Tình huống ngoại lệ hoặc điều kiện biên")
    consequence: str = Field(..., description="Hệ quả hoặc hành vi bất thường")
    exception_rule: str = Field(..., description="Cách xử lý hoặc quy tắc loại trừ")
    chunk_id: str
    exact_quote: str
    bloom_level: BloomLevel = "ANALYZE_EVALUATE"

class ConceptMap(BaseModel):
    core_definitions: List[CoreDefinition] = Field(default_factory=list)
    formulas_and_theorems: List[FormulaOrTheorem] = Field(default_factory=list)
    causal_relationships: List[CausalRelationship] = Field(default_factory=list)
    edge_cases: List[EdgeCase] = Field(default_factory=list)

class ExtractedKnowledgeBundle(BaseModel):
    document_id: str
    document_title: str
    total_chunks: int
    detected_topics: List[str] = Field(default_factory=list)
    chunks: List[ChunkMetadata] = Field(default_factory=list)
    concept_map: ConceptMap
