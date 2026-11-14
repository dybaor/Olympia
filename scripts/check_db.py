import sys
sys.path.insert(0, '.')
import sqlite3

for db_path in ['data/arena.db', 'dist/Olympic_Portable/data/arena.db', 'dist/OlympicArena/data/arena.db']:
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, title, file_type, extracted_bundle_json FROM documents")
        docs = cur.fetchall()
        print(f"--- DB: {db_path} ---")
        for doc_id, title, ftype, bundle_str in docs:
            has_cau_181 = 'Câu 181' in (bundle_str or '')
            has_thuat_ngu = 'Thuật ngữ nào sau đây' in (bundle_str or '')
            print(f"Doc {doc_id}: title='{title}', type={ftype}, has_cau_181={has_cau_181}, has_thuat_ngu={has_thuat_ngu}")
        
        cur.execute("SELECT id, document_id, match_mode, exam_json FROM exams")
        exams = cur.fetchall()
        for ex_id, d_id, mode, ex_json in exams:
            has_cau_181 = 'Câu 181' in (ex_json or '')
            has_thuat_ngu = 'Thuật ngữ nào sau đây' in (ex_json or '')
            print(f"Exam {ex_id} (doc={d_id}): has_cau_181={has_cau_181}, has_thuat_ngu={has_thuat_ngu}")
    except Exception as e:
        print(f"Error {db_path}: {e}")

