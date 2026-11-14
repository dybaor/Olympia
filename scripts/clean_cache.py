import sys
sys.path.insert(0, '.')
import sqlite3

for db_path in ['data/arena.db', 'dist/Olympic_Portable/data/arena.db', 'dist/OlympicArena/data/arena.db']:
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # Xóa các doc hoặc exam chứa "Thuật ngữ nào sau đây" hoặc "Câu 181" trong các bảng
        cur.execute("DELETE FROM exams WHERE exam_json LIKE '%Thuật ngữ nào sau đây%' OR exam_json LIKE '%Câu 181%'")
        cur.execute("DELETE FROM documents WHERE extracted_bundle_json LIKE '%Câu 181%'")
        cur.execute("DELETE FROM game_sessions WHERE id IN (SELECT id FROM game_sessions WHERE answers_log_json LIKE '%Thuật ngữ nào sau đây%')")
        conn.commit()
        print(f"Cleaned old cache in {db_path} successfully.")
    except Exception as e:
        print(f"Note on {db_path}: {e}")

