from __future__ import annotations

from edu_cs_core.storage.database import Base, engine
from edu_cs_core.storage import models  # noqa: F401
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.seed_role_templates import seed_role_templates


def bootstrap_database() -> None:
    Base.metadata.create_all(bind=engine)
    seed_role_templates(SessionLocal)
