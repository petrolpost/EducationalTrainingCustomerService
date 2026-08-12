from __future__ import annotations

from fastapi import FastAPI

from edu_cs_core.api.routes.feedback import router as feedback_router
from edu_cs_core.api.routes.replay_timeline import router as replay_timeline_router
from edu_cs_core.api.routes.replays import router as replays_router
from edu_cs_core.api.routes.review import router as review_router
from edu_cs_core.api.routes.signals import router as signals_router
from edu_cs_core.api.routes.config import router as config_router
from edu_cs_core.services.logging import configure_logging, get_logger, log_event
from edu_cs_core.storage.bootstrap import bootstrap_database


logger = get_logger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    bootstrap_database()
    app = FastAPI(title="edu-cs-core", version="0.1.0")

    @app.get("/health")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(replays_router)
    app.include_router(replay_timeline_router)
    app.include_router(feedback_router)
    app.include_router(signals_router)
    app.include_router(config_router)
    app.include_router(review_router)

    log_event(logger, "api.app.created", version=app.version, title=app.title)
    return app
