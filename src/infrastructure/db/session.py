import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_session() -> Session:
    """Factory for a new SQLAlchemy Session (used by the UoW)."""
    return SessionLocal()


def get_db():
    """
    FastAPI dependency: yields a session and closes it afterwards.
    Usage in routers: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
