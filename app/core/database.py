import json
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 15}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    raw_content = Column(Text, nullable=False)
    extracted_bundle_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ExamModel(Base):
    __tablename__ = "exams"

    id = Column(String, primary_key=True, index=True)
    document_id = Column(String, index=True)
    match_mode = Column(String, default="ARENA_COMPETITION")
    exam_json = Column(Text, nullable=False)
    critic_report_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class GameSessionModel(Base):
    __tablename__ = "game_sessions"

    id = Column(String, primary_key=True, index=True)
    exam_id = Column(String, index=True)
    match_mode = Column(String, default="ARENA_COMPETITION")
    practice_filter = Column(String, default="ALL_ROUNDS")
    total_score = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    completed_rounds = Column(Integer, default=0)
    is_finished = Column(Boolean, default=False)
    hints_used_count = Column(Integer, default=0)
    answers_log_json = Column(Text, default="[]")
    config_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
