from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DB_PATH = Path("backend/.data/edu_cs_core.sqlite3")


class Base(DeclarativeBase):
    """Shared declarative base for storage models."""


def build_database_url(path: Path | None = None) -> str:
    db_path = (path or DEFAULT_DB_PATH).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_path.as_posix()}"


engine = create_engine(build_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
