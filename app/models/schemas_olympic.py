from typing import List, Optional, Literal
from pydantic import BaseModel, Field

QuestionType = Literal[
    "speed_mcq",           # Vòng 1: Trắc nghiệm tốc độ
    "obstacle_clue",       # Vòng 2: Hàng ngang gợi ý chướng ngại vật
    "multi_hop_scenario",  # Vòng 3: Suy luận đa bước / tình huống
    "adversarial_essay"    # Vòng 4: Câu hỏi phản biện / bẫy / tự luận ngắn
]

BloomLevel = Literal["REMEMBER", "UNDERSTAND", "APPLY", "ANALYZE_EVALUATE"]
DifficultyLevel = Literal["EASY", "MEDIUM", "HARD", "EXTREME"]
MatchMode = Literal["ARENA_COMPETITION", "PRACTICE_DOJO"]
PracticeFilter = Literal["ALL_ROUNDS", "ONLY_ROUND_1", "ONLY_ROUND_2", "ONLY_ROUND_3", "ONLY_ROUND_4", "WEAK_AREAS_ONLY"]

class SourceCitation(BaseModel):
    chunk_id: str = Field(..., description="Mã đoạn chứa thông tin")
    exact_quote: str = Field(..., description="Trích dẫn đoạn văn gốc chứng minh đáp án đúng")
    page_or_section: str = Field(..., description="Vị trí trang hoặc tiêu đề mục")

class ProgressiveHints(BaseModel):
    level_1_hint: str = Field(..., description="Gợi ý tầng 1: Hướng tiếp cận khái niệm hoặc quy tắc liên quan")
    level_2_hint: str = Field(..., description="Gợi ý tầng 2: Chỉ ra dữ kiện then chốt, sát với đáp án đúng")

class OlympicQuestion(BaseModel):
    question_id: str
    round_number: int = Field(..., ge=1, le=4)
    question_type: QuestionType
    bloom_level: BloomLevel = "UNDERSTAND"
    difficulty: DifficultyLevel = "MEDIUM"
    prompt: str = Field(..., description="Nội dung câu hỏi")
    options: Optional[List[str]] = Field(default=None, description="Danh sách 4 lựa chọn cho trắc nghiệm")
    correct_answer: str = Field(..., description="Đáp án chính xác")
    acceptable_keywords: Optional[List[str]] = Field(
        default=None, 
        description="Các từ khóa chấp nhận được cho câu tự luận/điền từ ngắn"
    )
    explanation: str = Field(..., description="Lời giải thích chi tiết")
    step_by_step_explanation: List[str] = Field(
        default_factory=list,
        description="Từng bước suy luận logic bóc tách lời giải phục vụ chế độ Luyện tập"
    )
    progressive_hints: ProgressiveHints = Field(
        ...,
        description="2 tầng gợi ý tiến tiến phục vụ chế độ Luyện tập"
    )
    source_citation: SourceCitation
    time_limit_sec: int = Field(default=20, description="Thời gian giới hạn tính bằng giây")
    base_score: int = Field(default=10, description="Điểm cơ bản khi trả lời đúng")
    allows_star_of_hope: bool = Field(default=False, description="Được phép đặt Ngôi sao hy vọng (Vòng 4)")
    knowledge_dimension: str = Field(
        default="Concept", 
        description="Chiều kiến thức (Concept, Formula, Causality, EdgeCase, Synthesis)"
    )

class RoundConfig(BaseModel):
    round_number: int = Field(..., ge=1, le=4)
    difficulty: DifficultyLevel = "MEDIUM"
    time_limit_sec: int = Field(default=20, ge=5, le=120)
    question_count: int = Field(default=4, ge=1, le=100)

class UserMatchConfig(BaseModel):
    match_mode: MatchMode = "ARENA_COMPETITION"
    practice_filter: PracticeFilter = "ALL_ROUNDS"
    topic_filter: Optional[str] = Field(default=None, description="Lọc theo Chương/Phần cụ thể hoặc ALL")
    practice_order: Optional[str] = Field(default="sequential", description="Thứ tự luyện tập: sequential hoặc random")
    round_configs: List[RoundConfig] = Field(
        default_factory=lambda: [
            RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=8),
            RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=4),
            RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=30, question_count=4),
            RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=45, question_count=3),
        ]
    )

class OlympicRoundSet(BaseModel):
    round_number: int
    round_name: str
    round_theme: str
    difficulty: DifficultyLevel = "MEDIUM"
    time_limit_per_question_sec: int
    obstacle_keyword: Optional[str] = None  # Chỉ dành cho Vòng 2
    obstacle_clue_count: Optional[int] = None
    questions: List[OlympicQuestion] = Field(default_factory=list)

class FullOlympicExam(BaseModel):
    document_id: str
    document_title: str
    match_mode: MatchMode = "ARENA_COMPETITION"
    rounds: List[OlympicRoundSet] = Field(default_factory=list)
    total_questions: int = 0
