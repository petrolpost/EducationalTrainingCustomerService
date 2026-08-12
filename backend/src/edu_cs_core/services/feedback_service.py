from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel, Field, model_validator

from edu_cs_core.services.logging import get_logger, log_event
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.feedback_repository import FeedbackRepository


logger = get_logger(__name__)


class FeedbackCreate(BaseModel):
    session_id: str
    evaluation_id: str | None = None
    attribution_id: str | None = None
    feedback_type: str
    feedback_actor_kind: str | None = None
    feedback_actor_id: str | None = None
    feedback_payload: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_target_links(self) -> "FeedbackCreate":
        if not any([self.session_id, self.evaluation_id, self.attribution_id]):
            raise ValueError("feedback must target a session, evaluation, or attribution")
        return self


class FeedbackService:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory

    def add_feedback(self, payload: dict) -> dict:
        request = FeedbackCreate.model_validate(payload)
        with self._session_factory() as session:
            repository = FeedbackRepository(session)
            replay_session = repository.get_session(request.session_id)
            if replay_session is None:
                log_event(logger, "feedback.session.not_found", level=logging.WARNING, session_id=request.session_id)
                raise KeyError(request.session_id)

            if request.evaluation_id is not None:
                evaluation = repository.get_evaluation(request.evaluation_id)
                if evaluation is None or evaluation.session_id != request.session_id:
                    log_event(
                        logger,
                        "feedback.evaluation.invalid",
                        level=logging.WARNING,
                        session_id=request.session_id,
                        evaluation_id=request.evaluation_id,
                    )
                    raise ValueError("evaluation_id must belong to the target session")

            if request.attribution_id is not None:
                attribution = repository.get_attribution(request.attribution_id)
                if attribution is None:
                    log_event(
                        logger,
                        "feedback.attribution.not_found",
                        level=logging.WARNING,
                        session_id=request.session_id,
                        attribution_id=request.attribution_id,
                    )
                    raise ValueError("attribution_id must exist")
                if request.evaluation_id is not None and attribution.evaluation_id != request.evaluation_id:
                    log_event(
                        logger,
                        "feedback.attribution.mismatch",
                        level=logging.WARNING,
                        session_id=request.session_id,
                        evaluation_id=request.evaluation_id,
                        attribution_id=request.attribution_id,
                    )
                    raise ValueError("attribution_id must belong to evaluation_id")
                if request.evaluation_id is None:
                    evaluation = repository.get_evaluation(attribution.evaluation_id)
                    if evaluation is None or evaluation.session_id != request.session_id:
                        raise ValueError("attribution_id must belong to the target session")

            record = repository.create_feedback(request.model_dump())
            result = {
                "feedback_id": record.feedback_id,
                "session_id": record.session_id,
                "evaluation_id": record.evaluation_id,
                "attribution_id": record.attribution_id,
                "feedback_type": record.feedback_type,
                "feedback_actor_kind": record.feedback_actor_kind,
                "feedback_actor_id": record.feedback_actor_id,
                "feedback_payload": json.loads(record.feedback_payload),
            }
            session.commit()
        log_event(
            logger,
            "feedback.recorded",
            feedback_id=result["feedback_id"],
            session_id=result["session_id"],
            evaluation_id=result["evaluation_id"],
            attribution_id=result["attribution_id"],
            feedback_type=result["feedback_type"],
        )
        return result
