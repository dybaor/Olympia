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
templates = Jinja2Templates(directory=str(templates_dir))

app.include_router(docs_router)
app.include_router(game_router)
app.include_router(multiplayer_router)

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    html_file = templates_dir / "index.html"
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Dau Truong Tri Thuc - Olympic Arena"}

