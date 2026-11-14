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

def find_index_html() -> str | None:
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
                    return content
        except Exception:
            pass

    # Fallback: Quét tìm file index.html trong thư mục hiện tại
    try:
        for p in Path.cwd().rglob("index.html"):
            if "templates" in str(p) and p.is_file():
                try:
                    return p.read_text(encoding="utf-8")
                except Exception:
                    pass
    except Exception:
        pass

    return None

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    html_content = find_index_html()
    if html_content:
        return HTMLResponse(content=html_content)
    fallback_html = """<!DOCTYPE html>
    <html lang="vi">
    <head><meta charset="utf-8"><title>Đấu Trường Tri Thức</title></head>
    <body style="background:#0f172a; color:#f8fafc; font-family:sans-serif; text-align:center; padding-top:50px;">
        <h2>⚠️ Không tìm thấy giao diện index.html</h2>
        <p>Vui lòng đảm bảo thư mục <code>app/templates/index.html</code> hoặc <code>_internal/app/templates/index.html</code> tồn tại.</p>
        <button onclick="location.reload()" style="padding:10px 20px; font-weight:bold; cursor:pointer;">Tải lại trang</button>
    </body>
    </html>"""
    return HTMLResponse(content=fallback_html, status_code=200)

@app.post("/heartbeat")
@app.get("/heartbeat")
def heartbeat():
    return {"status": "alive"}

@app.websocket("/ws/{client_id}")
async def generic_ws_client(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint chung phục vụ kết nối kiểm tra, IDE livereload, hoặc preview sync.
    Chấp nhận mọi kết nối hợp lệ, ngăn chặn hoàn toàn lỗi 403 Forbidden.
    """
    await websocket.accept()
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

@app.websocket("/ws/{room_code}/{player_id}")
async def root_multiplayer_ws_alias(websocket: WebSocket, room_code: str, player_id: str):
    """Alias cho Multiplayer WebSocket tại root đường dẫn /ws/{room_code}/{player_id}"""
    from app.api.routes_multiplayer import websocket_multiplayer_endpoint
    await websocket_multiplayer_endpoint(websocket, room_code, player_id)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Dau Truong Tri Thuc - Olympic Arena"}

