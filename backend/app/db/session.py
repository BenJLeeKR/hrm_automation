from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# DATABASE_URL은 postgresql+psycopg(동기 드라이버) 스킴을 사용한다 (.env / alembic/env.py와 동일).
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI 의존성 — 요청 단위 DB 세션을 생성하고 종료 시 반드시 닫는다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
