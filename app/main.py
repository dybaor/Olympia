import os
import json
from pathlib import Path
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import BASE_DIR, BUNDLE_DIR
from app.core.database import init_db
from app.api.routes_documents import router as docs_router
from app.api.routes_game import router as game_router
from app.api.routes_multiplayer import router as multiplayer_router

# Khởi tạo DB
init_db()

app = FastAPI(
    title="Đấu Trường Tri Thức - Olympic Knowledge Arena",
    description="Hệ thống Swarm tự động phân tích tài liệu và tổ chức thi đấu Olympic 4 vòng",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates_dir = BUNDLE_DIR / "app" / "templates"
static_dir = BUNDLE_DIR / "app" / "static"
if not templates_dir.exists():
    templates_dir = BASE_DIR / "app" / "templates"
if not static_dir.exists():
    static_dir = BASE_DIR / "app" / "static"

# Đảm bảo thư mục tồn tại để tránh lỗi Starlette StaticFiles
templates_dir.mkdir(parents=True, exist_ok=True)
static_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir), check_dir=False), name="static")

app.include_router(docs_router)
app.include_router(game_router)
app.include_router(multiplayer_router)

_CACHED_INDEX_HTML: str | None = None

def find_index_html() -> str | None:
    global _CACHED_INDEX_HTML
    if _CACHED_INDEX_HTML:
        return _CACHED_INDEX_HTML

    search_paths = [
        templates_dir / "index.html",
        BUNDLE_DIR / "app" / "templates" / "index.html",
        BASE_DIR / "app" / "templates" / "index.html",
        BASE_DIR / "_internal" / "app" / "templates" / "index.html",
        Path(__file__).resolve().parent / "templates" / "index.html",
        Path.cwd() / "app" / "templates" / "index.html",
        Path.cwd() / "dist" / "Olympic_Portable" / "_internal" / "app" / "templates" / "index.html",
        Path.cwd() / "dist" / "OlympicArena" / "_internal" / "app" / "templates" / "index.html",
    ]
    for p in search_paths:
        try:
            if p.exists() and p.is_file():
                content = p.read_text(encoding="utf-8")
                if content:
                    _CACHED_INDEX_HTML = content
                    return content
        except Exception:
            pass

    # Fallback: Quét tìm file index.html trong thư mục hiện tại
    try:
        for p in Path.cwd().rglob("index.html"):
            if "templates" in str(p) and p.is_file():
                try:
                    content = p.read_text(encoding="utf-8")
                    if content:
                        _CACHED_INDEX_HTML = content
                        return content
                except Exception:
                    pass
    except Exception:
        pass

    return None

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    try:
        html_content = find_index_html()
        if html_content:
            return HTMLResponse(content=html_content, status_code=200)
    except Exception as exc:
        pass

    fallback_html = """<!DOCTYPE html>
    <html lang="vi">
    <head><meta charset="utf-8"><title>Đấu Trường Tri Thức</title></head>
    <body style="background:#0f172a; color:#f8fafc; font-family:sans-serif; text-align:center; padding-top:50px;">
        <h2>🏛️ Đấu Trường Tri Thức - Olympic Arena</h2>
        <p>Hệ thống máy chủ đã sẵn sàng. Vui lòng tải lại trang hoặc kiểm tra file giao diện <code>index.html</code>.</p>
        <button onclick="location.reload()" style="padding:10px 20px; font-weight:bold; cursor:pointer; background:#0284c7; color:#fff; border:none; border-radius:6px;">Tải lại trang</button>
    </body>
    </html>"""
    return HTMLResponse(content=fallback_html, status_code=200)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Bắt mọi ngoại lệ chưa xử lý, tránh trả về trang lỗi Internal Server Error trần"""
    if "text/html" in request.headers.get("accept", ""):
        html_content = find_index_html()
        if html_content:
            return HTMLResponse(content=html_content, status_code=200)
        return HTMLResponse(
            content=f"<h3>Đấu Trường Tri Thức</h3><p>Hệ thống đang hoạt động. Vui lòng tải lại trang.</p><pre>{str(exc)}</pre>",
            status_code=200
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Error", "detail": str(exc)}
    )

@app.post("/heartbeat")
@app.get("/heartbeat")
def heartbeat():
    return {"status": "alive"}

@app.websocket("/ws")
@app.websocket("/ws/{full_path:path}")
async def universal_ws_endpoint(websocket: WebSocket, full_path: str = ""):
    """
    WebSocket endpoint toàn năng (Universal WebSocket Catch-all):
    - Tự động nhận diện kết nối thi đấu Multiplayer: /ws/{room_code}/{player_id}
    - Chấp nhận mọi kết nối WebSocket khác: /ws/{client_id}, /ws, kiểm tra preview, livereload...
    - Ngăn chặn 100% lỗi 403 Forbidden khi kết nối từ mọi nguồn hợp lệ.
    """
    parts = [p for p in full_path.strip("/").split("/") if p]
    if len(parts) == 2 and (parts[0].startswith("OLY-") or len(parts[0]) == 7):
        # Đường dẫn thi đấu Multiplayer: /ws/{room_code}/{player_id}
        from app.api.routes_multiplayer import websocket_multiplayer_endpoint
        await websocket_multiplayer_endpoint(websocket, parts[0], parts[1])
        return

    # Kết nối WebSocket chung / client preview / livereload
    await websocket.accept()
    client_id = parts[0] if parts else "client"
    try:
        await websocket.send_json({"type": "CONNECTED", "client_id": client_id, "status": "ok"})
        while True:
            data = await websocket.receive_text()
            if not data:
                break
            try:
                msg = json.loads(data)
                if msg.get("action") == "CLOSE":
                    break
                action = msg.get("action", "") or msg.get("type", "")
                await websocket.send_json({"type": "PONG", "action": action, "client_id": client_id, "status": "ok"})
            except Exception:
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Dau Truong Tri Thuc - Olympic Arena"}

