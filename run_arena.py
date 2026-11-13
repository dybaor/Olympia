import sys
import uvicorn

# Đảm bảo in UTF-8 không bị lỗi trên Windows console
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
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
    uvicorn.run(app, host="127.0.0.1", port=8000)
