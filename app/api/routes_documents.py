import os
import json
import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import get_db, DocumentModel, ExamModel
from app.models.schemas_extracted import ExtractedKnowledgeBundle, ConceptMap, ChunkMetadata
from app.skills.doc_parser import KnowledgeGraphExtractor
from app.services.swarm_orchestrator import SwarmOrchestrator
from app.services.md_quiz_parser import DirectMDQuizParser

router = APIRouter(prefix="/api/documents", tags=["documents"])
extractor = KnowledgeGraphExtractor()
orchestrator = SwarmOrchestrator()

@router.post("/upload")
async def upload_document(
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Tải lên 1 hoặc nhiều tài liệu (PDF, DOCX, MD, TXT) cùng lúc (Multi-file Upload):
    - Tự động nhận diện cấu trúc đề trắc nghiệm Markdown (Direct_MD_Quiz_Parser).
    - Tự động gộp dữ liệu câu hỏi, chuyên đề và phân tầng tư duy từ toàn bộ các file được gửi lên.
    - Đánh lại ID câu hỏi liên tục, gắn nhãn tên file nguồn vào chuyên đề khi có nhiều file.
    - Tương thích ngược hoàn toàn với việc upload đơn 1 file.
    """
    upload_list: List[UploadFile] = []
    if files:
        upload_list.extend([f for f in files if f.filename])
    if file and file.filename and file not in upload_list:
        upload_list.append(file)

    if not upload_list:
        raise HTTPException(
            status_code=400, 
            detail="Vui lòng chọn ít nhất một tệp tài liệu (PDF, DOCX, MD, TXT)."
        )

    # Kiểm tra định dạng tất cả file
    valid_exts = [".pdf", ".docx", ".md", ".txt"]
    for uf in upload_list:
        ext = Path(uf.filename).suffix.lower()
        if ext not in valid_exts:
            raise HTTPException(
                status_code=400,
                detail=f"Định dạng '{ext}' của file '{uf.filename}' không được hỗ trợ. Vui lòng tải lên PDF, DOCX, MD hoặc TXT."
            )

    doc_id = f"DOC_{uuid.uuid4().hex[:8]}"
    saved_files = []

    try:
        # Lưu các file vào thư mục UPLOAD_DIR bằng async read an toàn
        for uf in upload_list:
            safe_name = uf.filename.replace(" ", "_")
            file_save_path = UPLOAD_DIR / f"{doc_id}_{safe_name}"
            content_bytes = await uf.read()
            file_save_path.write_bytes(content_bytes)
            saved_files.append((uf.filename, file_save_path, content_bytes))

        # Phân loại và bóc tách từng file
        md_quiz_files = []
        theory_bundles = []

        for fname, fpath, cbytes in saved_files:
            ext = fpath.suffix.lower()
            if ext in [".md", ".txt"]:
                content = cbytes.decode("utf-8", errors="ignore")
                if DirectMDQuizParser.is_markdown_quiz(content):
                    md_quiz_files.append({"filename": fname, "content": content, "path": str(fpath)})
                    continue

            # File lý thuyết thông thường: chạy trích xuất KnowledgeGraphExtractor
            sub_bundle = extractor.process_document(str(fpath), doc_id=f"{doc_id}_{len(theory_bundles)}")
            theory_bundles.append(sub_bundle)

        # XÂY DỰNG BUNDLE TỔNG HỢP (SMART MERGING)
        combined_title = upload_list[0].filename if len(upload_list) == 1 else " + ".join([uf.filename for uf in upload_list[:3]])
        if len(upload_list) > 3:
            combined_title += f" (+{len(upload_list)-3} tệp khác)"

        if md_quiz_files:
            # Có ít nhất 1 file là bộ đề trắc nghiệm nguyên bản
            if len(md_quiz_files) == 1 and not theory_bundles:
                bundle = DirectMDQuizParser.build_knowledge_bundle(
                    content=md_quiz_files[0]["content"],
                    doc_id=doc_id,
                    doc_title=md_quiz_files[0]["filename"]
                )
            else:
                bundle = DirectMDQuizParser.build_merged_knowledge_bundle(
                    files_data=md_quiz_files,
                    doc_id=doc_id,
                    combined_title=combined_title
                )

            # Nếu có thêm các file lý thuyết đi kèm, gộp các chunk và concept_map vào
            if theory_bundles:
                for tb in theory_bundles:
                    bundle.chunks.extend(tb.chunks)
                    bundle.concept_map.core_definitions.extend(tb.concept_map.core_definitions)
                    bundle.concept_map.formulas_and_theorems.extend(tb.concept_map.formulas_and_theorems)
                    bundle.concept_map.causal_relationships.extend(tb.concept_map.causal_relationships)
                    bundle.concept_map.edge_cases.extend(tb.concept_map.edge_cases)
                    for term in tb.concept_map.domain_glossary:
                        if term not in bundle.concept_map.domain_glossary:
                            bundle.concept_map.domain_glossary.append(term)
                bundle.total_chunks = len(bundle.chunks)
        else:
            # Toàn bộ là file lý thuyết: Gộp các theory bundles
            if len(theory_bundles) == 1:
                bundle = theory_bundles[0]
                bundle.document_id = doc_id
            else:
                merged_chunks = []
                merged_topics = []
                all_defs = []
                all_forms = []
                all_caus = []
                all_edge = []
                all_gloss = []
                for tb in theory_bundles:
                    merged_chunks.extend(tb.chunks)
                    for t in tb.detected_topics:
                        if t not in merged_topics:
                            merged_topics.append(t)
                    all_defs.extend(tb.concept_map.core_definitions)
                    all_forms.extend(tb.concept_map.formulas_and_theorems)
                    all_caus.extend(tb.concept_map.causal_relationships)
                    all_edge.extend(tb.concept_map.edge_cases)
                    for term in tb.concept_map.domain_glossary:
                        if term not in all_gloss:
                            all_gloss.append(term)

                bundle = ExtractedKnowledgeBundle(
                    document_id=doc_id,
                    document_title=combined_title,
                    total_chunks=len(merged_chunks),
                    detected_topics=merged_topics,
                    chunks=merged_chunks,
                    concept_map=ConceptMap(
                        core_definitions=all_defs,
                        formulas_and_theorems=all_forms,
                        causal_relationships=all_caus,
                        edge_cases=all_edge,
                        domain_glossary=all_gloss
                    ),
                    is_direct_quiz=False,
                    total_direct_questions=0
                )

        # Lưu Document vào Database
        primary_file_path = str(saved_files[0][1])
        doc_record = DocumentModel(
            id=doc_id,
            title=bundle.document_title,
            file_type="multi" if len(upload_list) > 1 else Path(upload_list[0].filename).suffix.lower(),
            file_path=primary_file_path,
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
            "file_count": len(upload_list),
            "files": [uf.filename for uf in upload_list],
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
