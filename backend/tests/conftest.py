from __future__ import annotations

import json
from pathlib import Path

import pytest

from edu_cs_core.storage.bootstrap import bootstrap_database
from edu_cs_core.storage.database import Base, SessionLocal, engine


@pytest.fixture(autouse=True)
def reset_database() -> None:
    Base.metadata.drop_all(bind=engine)
    bootstrap_database()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def replay_payload() -> dict:
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "replay_session.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


@pytest.fixture()
def session_factory():
    return SessionLocal
