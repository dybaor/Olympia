import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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
    ]
    for p in search_paths:
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                pass
    return None

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    html_content = find_index_html()
    if html_content:
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Olympic Knowledge Arena</h1><p>index.html not found. Vui long kiem tra file template.</p>", status_code=500)

@app.post("/heartbeat")
def heartbeat():
    return {"status": "alive"}

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Dau Truong Tri Thuc - Olympic Arena"}

