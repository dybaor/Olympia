from typing import List, Optional, Literal
from pydantic import BaseModel, Field

VerificationStatus = Literal["APPROVED", "REJECTED_NEEDS_REVISION"]

class QuestionAuditScore(BaseModel):
    citation_fidelity: float = Field(..., ge=0, le=100, description="Độ trung thực so với đoạn trích (0-100)")
    distractor_quality: float = Field(..., ge=0, le=100, description="Chất lượng phương án gây nhiễu (0-100)")
    clarity_and_unambiguity: float = Field(..., ge=0, le=100, description="Độ rõ ràng, không đa nghĩa (0-100)")
    cognitive_depth: float = Field(..., ge=0, le=100, description="Độ sâu tư duy (tránh copy-paste nguyên văn)")

class QuestionAuditResult(BaseModel):
    question_id: str
    status: VerificationStatus
    scores: QuestionAuditScore
    hallucination_detected: bool = False
    is_verbatim_copy: bool = False
    is_ambiguous: bool = False
    critic_notes: str = ""
    remedy_instruction: Optional[str] = None

class CriticEvaluationReport(BaseModel):
    round_number: int
    all_passed: bool
    retry_attempt: int = 0
    passed_count: int = 0
    rejected_count: int = 0
    audit_results: List[QuestionAuditResult] = Field(default_factory=list)
    summary_verdict: str = ""

