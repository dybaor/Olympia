import os
import json
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import get_db, DocumentModel, ExamModel
from app.skills.doc_parser import KnowledgeGraphExtractor
from app.services.swarm_orchestrator import SwarmOrchestrator
from app.services.md_quiz_parser import DirectMDQuizParser

router = APIRouter(prefix="/api/documents", tags=["documents"])
extractor = KnowledgeGraphExtractor()
orchestrator = SwarmOrchestrator()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Tải lên tài liệu (PDF, DOCX, MD, TXT):
    - Tự động nhận diện cấu trúc đề trắc nghiệm Markdown (Direct_MD_Quiz_Parser).
    - Nếu là file trắc nghiệm chuẩn: Chuyển sang Fast-Import tức thì, 100% chính xác, không gọi LLM.
    - Nếu là tài liệu lý thuyết: Kích hoạt Agent 1 phân tầng nhận thức Bloom như cũ.
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".md", ".txt"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Định dạng {ext} không được hỗ trợ. Vui lòng tải lên PDF, DOCX, MD hoặc TXT."
        )

    doc_id = f"DOC_{uuid.uuid4().hex[:8]}"
    file_save_path = UPLOAD_DIR / f"{doc_id}_{file.filename}"

    with open(file_save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # XÓA BỘ ĐỀ VÀ KẾT QUẢ CŨ CÙNG TÊN ĐỂ TRÁNH DỮ LIỆU CACHE CŨ
        old_docs = db.query(DocumentModel).filter(DocumentModel.title == file.filename).all()
        for od in old_docs:
            db.query(ExamModel).filter(ExamModel.document_id == od.id).delete()
            db.delete(od)
        db.commit()

        # KIỂM TRA TỰ ĐỘNG: Có phải file Markdown bộ đề trắc nghiệm sẵn không?
        is_direct_md = False
        if ext in [".md", ".txt"]:
            content = file_save_path.read_text(encoding="utf-8")
            if DirectMDQuizParser.is_markdown_quiz(content):
                is_direct_md = True
                # KHÓA HOÀN TOÀN LUỒNG EXTRACTOR/GENERATOR: Chỉ nạp 100% câu hỏi gốc
                bundle = DirectMDQuizParser.build_knowledge_bundle(
                    content=content,
                    doc_id=doc_id,
                    doc_title=file.filename
                )

        if not is_direct_md:
            # Kích hoạt Agent 1: Bóc tách tri thức & phân tầng Bloom thông thường cho tài liệu lý thuyết
            bundle = extractor.process_document(str(file_save_path), doc_id=doc_id)

        # Lưu Document vào Database
        doc_record = DocumentModel(
            id=doc_id,
            title=bundle.document_title,
            file_type=ext,
            file_path=str(file_save_path),
            raw_content="",
            extracted_bundle_json=bundle.model_dump_json(),
        )
        db.add(doc_record)
        db.commit()

        # Đếm số lượng theo thang nhận thức Bloom
        bloom_counts = {"REMEMBER": 0, "UNDERSTAND": 0, "APPLY": 0, "ANALYZE_EVALUATE": 0}
        for d in bundle.concept_map.core_definitions:
            bloom_counts[d.bloom_level] = bloom_counts.get(d.bloom_level, 0) + 1
        for f in bundle.concept_map.formulas_and_theorems:
            bloom_counts[f.bloom_level] = bloom_counts.get(f.bloom_level, 0) + 1
        for c in bundle.concept_map.causal_relationships:
            bloom_counts[c.bloom_level] = bloom_counts.get(c.bloom_level, 0) + 1
        for e in bundle.concept_map.edge_cases:
            bloom_counts[e.bloom_level] = bloom_counts.get(e.bloom_level, 0) + 1

        return {
            "status": "success",
            "document_id": doc_id,
            "title": bundle.document_title,
            "is_direct_quiz": bundle.is_direct_quiz,
            "total_quiz_questions": bundle.total_direct_questions if bundle.is_direct_quiz else 0,
            "topics": bundle.direct_quiz_topics if bundle.is_direct_quiz else bundle.detected_topics,
            "total_chunks": bundle.total_chunks,
            "bloom_taxonomy_counts": bloom_counts,
            "concept_counts": {
                "definitions": len(bundle.concept_map.core_definitions),
                "formulas": len(bundle.concept_map.formulas_and_theorems),
                "causals": len(bundle.concept_map.causal_relationships),
                "edge_cases": len(bundle.concept_map.edge_cases),
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi trích xuất tài liệu: {str(e)}")

@router.get("/{doc_id}/concept-map")
def get_concept_map(doc_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu")
    bundle = json.loads(doc.extracted_bundle_json)
    return bundle.get("concept_map")

@router.get("/exam/{exam_id}")
def get_exam_details(exam_id: str, db: Session = Depends(get_db)):
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề thi")
    return json.loads(exam.exam_json)

@router.get("/exam/{exam_id}/critic-report")
def get_critic_report(exam_id: str, db: Session = Depends(get_db)):
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Không tìm thấy đề thi")
    return json.loads(exam.critic_report_json or "{}")
