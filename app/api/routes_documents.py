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
    Agent 1 (Knowledge_Graph_Extractor) chạy ngay lập tức để trích xuất tri thức & phân tầng Bloom.
    Lưu trữ và mở phòng cấu hình (Match Lobby) để người dùng chọn chế độ & độ khó.
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
        # Kích hoạt Agent 1: Bóc tách tri thức & phân tầng Bloom
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
