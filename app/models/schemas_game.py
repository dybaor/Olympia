from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class AnswerSubmission(BaseModel):
    session_id: str
    round_number: int
    question_id: str
    user_answer: str
    time_taken_sec: float
    star_of_hope_activated: bool = False
    used_hints_count: int = 0
    is_practice: bool = False

class HintRequest(BaseModel):
    session_id: str
    question_id: str
    hint_level: int = Field(..., ge=1, le=2, description="Cấp độ gợi ý: 1 hoặc 2")

class HintResponse(BaseModel):
    question_id: str
    hint_level: int
    hint_text: str
    hints_remaining: int

class ScoreFeedback(BaseModel):
    is_correct: bool
    base_points: int
    speed_bonus: int
    streak_bonus: int
    star_of_hope_multiplier: int
    total_delta_score: int
    current_total_score: int
    current_streak: int
    correct_answer: str
    explanation: str
    step_by_step_explanation: List[str] = Field(default_factory=list)
    source_citation: Dict[str, str]
    time_expired: bool = False

class DimensionScore(BaseModel):
    dimension_name: str
    total_questions: int
    correct_count: int
    accuracy_percentage: float
    evaluation: str

class GameSessionSummary(BaseModel):
    session_id: str
    document_title: str
    match_mode: str = "ARENA_COMPETITION"
    total_score: int
    max_streak: int
    time_spent_sec: float
    hints_used_total: int = 0
    dimension_analytics: List[DimensionScore]
    strengths: List[str]
    knowledge_gaps: List[str]
    actionable_recommendations: List[str]
