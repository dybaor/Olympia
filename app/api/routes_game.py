import json
import uuid
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db, DocumentModel, ExamModel, GameSessionModel
from app.models.schemas_extracted import ExtractedKnowledgeBundle
from app.models.schemas_olympic import FullOlympicExam, OlympicQuestion, UserMatchConfig
from app.models.schemas_game import (
    AnswerSubmission,
    ScoreFeedback,
    GameSessionSummary,
    HintRequest,
    HintResponse,
)
from app.services.game_engine import PracticeAndArenaEngine
from app.skills.round_architect import DynamicOlympicArchitect
from app.skills.fact_critic import AdversarialFactChecker

router = APIRouter(prefix="/api/game", tags=["game"])

@router.post("/setup-match")
def setup_match(
    document_id: str,
    config: UserMatchConfig,
    db: Session = Depends(get_db)
):
    """
    Phòng cấu hình trước trận đấu (Pre-Match Setup / Match Lobby):
    Nhận UserMatchConfig (độ khó và thời gian từng vòng, chế độ Thi đấu vs Luyện tập).
    Sinh đề thi tương ứng cuốn chiếu và khởi tạo GameSession.
    """
    doc_record = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not doc_record:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu gốc")

    bundle = ExtractedKnowledgeBundle.model_validate_json(doc_record.extracted_bundle_json)

    critic_reports = {}
    if bundle.is_direct_quiz:
        from app.services.md_quiz_parser import DirectMDQuizParser
        exam = DirectMDQuizParser.build_olympic_exam(bundle, config)
    else:
        # Khởi tạo Agent 2 và Agent 3 sinh đề theo cấu hình
        architect = DynamicOlympicArchitect(bundle)
        critic = AdversarialFactChecker(bundle)

        exam = architect.generate_full_olympic_exam(config)

        # Thẩm định chất lượng qua Critic
        for r in exam.rounds:
            critic_reports[r.round_number] = critic.audit_round(r)

    exam_id = f"EXAM_{uuid.uuid4().hex[:8]}"
    critic_dict = {str(k): v.model_dump() for k, v in critic_reports.items()}

    exam_record = ExamModel(
        id=exam_id,
        document_id=document_id,
        match_mode=config.match_mode,
        exam_json=exam.model_dump_json(),
        critic_report_json=json.dumps(critic_dict, ensure_ascii=False),
    )
    db.add(exam_record)

    # Khởi tạo Session
    session_id = f"SESS_{uuid.uuid4().hex[:8]}"
    new_session = GameSessionModel(
        id=session_id,
        exam_id=exam_id,
        match_mode=config.match_mode,
        practice_filter=config.practice_filter,
        total_score=0,
        current_streak=0,
        max_streak=0,
        completed_rounds=0,
        is_finished=False,
        hints_used_count=0,
        answers_log_json="[]",
        config_json=config.model_dump_json(),
    )
    db.add(new_session)
    db.commit()

    # Lọc các vòng theo practice_filter nếu có
    selected_rounds = exam.rounds
    if config.match_mode == "PRACTICE_DOJO":
        if config.practice_filter == "ONLY_ROUND_1":
            selected_rounds = [r for r in exam.rounds if r.round_number == 1]
        elif config.practice_filter == "ONLY_ROUND_2":
            selected_rounds = [r for r in exam.rounds if r.round_number == 2]
        elif config.practice_filter == "ONLY_ROUND_3":
            selected_rounds = [r for r in exam.rounds if r.round_number == 3]
        elif config.practice_filter == "ONLY_ROUND_4":
            selected_rounds = [r for r in exam.rounds if r.round_number == 4]

    # Chuẩn bị payload an toàn gửi client (ẩn đáp án đúng)
    client_rounds = []
    for r in selected_rounds:
        client_questions = []
        for q in r.questions:
            q_dict = q.model_dump()
            q_dict.pop("correct_answer", None)
            q_dict.pop("acceptable_keywords", None)
            q_dict.pop("explanation", None)
            # Nếu là Arena thì giấu cả hints, nếu là Practice thì giữ để xem qua endpoint /get-hint
            q_dict["has_hints"] = (config.match_mode == "PRACTICE_DOJO")
            client_questions.append(q_dict)

        r_dict = r.model_dump()
        r_dict["questions"] = client_questions
        if r_dict.get("obstacle_keyword"):
            r_dict["obstacle_length"] = len(r_dict["obstacle_keyword"].replace(" ", ""))
            r_dict.pop("obstacle_keyword", None)
        client_rounds.append(r_dict)

    return {
        "session_id": session_id,
        "exam_id": exam_id,
        "document_title": exam.document_title,
        "match_mode": config.match_mode,
        "practice_filter": config.practice_filter,
        "total_rounds": len(client_rounds),
        "rounds": client_rounds,
    }

@router.post("/get-hint", response_model=HintResponse)
def get_hint_for_question(req: HintRequest, db: Session = Depends(get_db)):
    """
    Lấy gợi ý 2 tầng (chỉ mở khóa ở chế độ Luyện tập - Practice Dojo).
    """
    session = db.query(GameSessionModel).filter(GameSessionModel.id == req.session_id).first()
    if not session or session.is_finished:
        raise HTTPException(status_code=400, detail="Phiên thi không hợp lệ")

    if session.match_mode == "ARENA_COMPETITION":
        raise HTTPException(status_code=403, detail="Chế độ Thi đấu Olympic khóa hoàn toàn chức năng xem gợi ý!")

    exam_record = db.query(ExamModel).filter(ExamModel.id == session.exam_id).first()
    exam = FullOlympicExam.model_validate_json(exam_record.exam_json)

    target_q = None
    for r in exam.rounds:
        for q in r.questions:
            if q.question_id == req.question_id:
                target_q = q
                break
        if target_q:
            break

    if not target_q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")

    session.hints_used_count += 1
    db.commit()

    return PracticeAndArenaEngine.get_hint(
        question=target_q,
        hint_level=req.hint_level,
        match_mode=session.match_mode
    )

@router.post("/generate-variant")
def generate_variant_question(session_id: str, question_id: str, db: Session = Depends(get_db)):
    """
    Tạo biến thể câu hỏi tương tự phục vụ Luyện tập (Practice Dojo).
    """
    session = db.query(GameSessionModel).filter(GameSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=400, detail="Phiên luyện tập không hợp lệ")

    exam_record = db.query(ExamModel).filter(ExamModel.id == session.exam_id).first()
    doc_record = db.query(DocumentModel).filter(DocumentModel.id == exam_record.document_id).first()
    bundle = ExtractedKnowledgeBundle.model_validate_json(doc_record.extracted_bundle_json)

    exam = FullOlympicExam.model_validate_json(exam_record.exam_json)
    target_q = None
    target_round = None
    for r in exam.rounds:
        for q in r.questions:
            if q.question_id == question_id:
                target_q = q
                target_round = r
                break
        if target_q:
            break

    if not target_q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi")

    architect = DynamicOlympicArchitect(bundle)
    variant_q = architect.generate_question_variant(target_q)

    # Thêm câu hỏi biến thể vào exam lưu trữ
    target_round.questions.append(variant_q)
    exam_record.exam_json = exam.model_dump_json()
    db.commit()

    safe_variant = variant_q.model_dump()
    safe_variant.pop("correct_answer", None)
    safe_variant.pop("explanation", None)
    return safe_variant

@router.post("/submit-answer", response_model=ScoreFeedback)
def submit_answer(submission: AnswerSubmission, db: Session = Depends(get_db)):
    session = db.query(GameSessionModel).filter(GameSessionModel.id == submission.session_id).first()
    if not session or session.is_finished:
        raise HTTPException(status_code=400, detail="Phiên thi không hợp lệ hoặc đã kết thúc")

    exam_record = db.query(ExamModel).filter(ExamModel.id == session.exam_id).first()
    exam = FullOlympicExam.model_validate_json(exam_record.exam_json)

    target_q: OlympicQuestion = None
    for r in exam.rounds:
        for q in r.questions:
            if q.question_id == submission.question_id:
                target_q = q
                break
        if target_q:
            break

    if not target_q:
        raise HTTPException(status_code=404, detail="Không tìm thấy câu hỏi trong đề thi")

    feedback = PracticeAndArenaEngine.evaluate_answer(
        submission=submission,
        question=target_q,
        current_total_score=session.total_score,
        current_streak=session.current_streak,
        match_mode=session.match_mode,
    )

    session.total_score = feedback.current_total_score
    session.current_streak = feedback.current_streak
    if feedback.current_streak > session.max_streak:
        session.max_streak = feedback.current_streak

    logs = json.loads(session.answers_log_json)
    logs.append({
        "round_number": submission.round_number,
        "question_id": submission.question_id,
        "user_answer": submission.user_answer,
        "is_correct": feedback.is_correct,
        "delta_score": feedback.total_delta_score,
        "time_taken_sec": submission.time_taken_sec,
        "star_of_hope_activated": submission.star_of_hope_activated,
        "time_expired": feedback.time_expired,
        "used_hints": submission.used_hints_count,
    })
    session.answers_log_json = json.dumps(logs)
    db.commit()

    return feedback

@router.post("/solve-obstacle")
def solve_obstacle(
    session_id: str,
    guessed_keyword: str,
    clues_opened: int,
    db: Session = Depends(get_db)
):
    session = db.query(GameSessionModel).filter(GameSessionModel.id == session_id).first()
    if not session or session.is_finished:
        raise HTTPException(status_code=400, detail="Phiên thi không hợp lệ")

    exam_record = db.query(ExamModel).filter(ExamModel.id == session.exam_id).first()
    exam = FullOlympicExam.model_validate_json(exam_record.exam_json)

    r2 = next((r for r in exam.rounds if r.round_number == 2), None)
    if not r2 or not r2.obstacle_keyword:
        raise HTTPException(status_code=400, detail="Không có vòng vượt chướng ngại vật")

    actual_kw = r2.obstacle_keyword.strip().lower().replace(" ", "")
    guess = guessed_keyword.strip().lower().replace(" ", "")

    is_correct = (actual_kw == guess)
    points = 0
    if is_correct:
        if clues_opened <= 1:
            points = 80
        elif clues_opened == 2:
            points = 60
        else:
            points = 40
        session.total_score += points
        db.commit()

    return {
        "is_correct": is_correct,
        "points_awarded": points,
        "actual_keyword": r2.obstacle_keyword,
        "current_total_score": session.total_score,
    }

@router.get("/topics")
def get_document_topics(document_id: str, db: Session = Depends(get_db)):
    """
    Lấy danh sách các chủ đề (topics/sections) kèm số lượng câu hỏi của từng chủ đề
    để hỗ trợ bộ lọc luyện tập theo chuyên đề trong Practice Dojo.
    """
    doc_record = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if not doc_record:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu gốc")

    bundle = ExtractedKnowledgeBundle.model_validate_json(doc_record.extracted_bundle_json)
    
    topics_list = []
    total_q = bundle.total_direct_questions or 0

    if bundle.is_direct_quiz:
        counts = getattr(bundle, "topic_question_counts", None) or {}
        # Nếu chưa có topic_question_counts (tài liệu parse cũ), đếm từ direct_quiz_questions_json
        if not counts and bundle.direct_quiz_questions_json:
            try:
                raw_q = json.loads(bundle.direct_quiz_questions_json)
                for item in raw_q:
                    sec = item.get("source_citation", {}).get("page_or_section", "Chung")
                    counts[sec] = counts.get(sec, 0) + 1
            except Exception:
                pass
        
        # Duyệt qua direct_quiz_topics hoặc detected_topics
        all_topics = bundle.direct_quiz_topics or bundle.detected_topics or list(counts.keys())
        for top in all_topics:
            c = counts.get(top, 0)
            topics_list.append({
                "topic_name": top,
                "question_count": c
            })
        if total_q == 0 and counts:
            total_q = sum(counts.values())
    else:
        for top in bundle.detected_topics:
            c = len([ch for ch in bundle.chunks if ch.page_or_section == top])
            topics_list.append({
                "topic_name": top,
                "question_count": max(1, c * 5)
            })
        total_q = sum(t["question_count"] for t in topics_list)

    return {
        "document_id": document_id,
        "document_title": bundle.document_title,
        "total_questions": total_q,
        "topics": topics_list
    }

@router.post("/finish", response_model=GameSessionSummary)
def finish_game_session(session_id: str, time_spent_sec: float = 120.0, db: Session = Depends(get_db)):
    session = db.query(GameSessionModel).filter(GameSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiên thi")

    exam_record = db.query(ExamModel).filter(ExamModel.id == session.exam_id).first()
    exam = FullOlympicExam.model_validate_json(exam_record.exam_json)

    session.is_finished = True
    db.commit()

    logs = json.loads(session.answers_log_json)

    summary = PracticeAndArenaEngine.generate_analytics(
        session_id=session_id,
        exam=exam,
        answer_logs=logs,
        total_score=session.total_score,
        max_streak=session.max_streak,
        time_spent=time_spent_sec,
        hints_used=session.hints_used_count,
        match_mode=session.match_mode,
    )

    return summary
