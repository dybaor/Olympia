import sys
import threading
import time
import webbrowser
import uvicorn

# Đảm bảo in UTF-8 không bị lỗi trên Windows console
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def open_browser():
    time.sleep(1.2)
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass

if __name__ == "__main__":
    from app.main import app
    print("=" * 65)
    print("  🏛️   ĐẤU TRƯỜNG TRI THỨC - OLYMPIC KNOWLEDGE ARENA")
    print("  🤖   Hệ thống Swarm AI phân tích tri thức & Đấu trường 4 vòng")
    print("  🌐   Đang phục vụ tại: http://localhost:8000")
    print("  💡   Nhấn Ctrl + C để dừng máy chủ")
    print("=" * 65)
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
