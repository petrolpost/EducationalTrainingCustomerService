from __future__ import annotations

import json
from uuid import uuid4

from edu_cs_core.storage.models import AttributionRecordModel, EvaluationRecordModel, FeedbackRecordModel, ReplaySessionModel


class FeedbackRepository:
    def __init__(self, session) -> None:
        self.session = session

    def get_session(self, session_id: str) -> ReplaySessionModel | None:
        return self.session.get(ReplaySessionModel, session_id)

    def get_evaluation(self, evaluation_id: str) -> EvaluationRecordModel | None:
        return self.session.get(EvaluationRecordModel, evaluation_id)

    def get_attribution(self, attribution_id: str) -> AttributionRecordModel | None:
        return self.session.get(AttributionRecordModel, attribution_id)

    def create_feedback(self, payload: dict) -> FeedbackRecordModel:
        model = FeedbackRecordModel(
            feedback_id=str(uuid4()),
            session_id=payload["session_id"],
            evaluation_id=payload.get("evaluation_id"),
            attribution_id=payload.get("attribution_id"),
            feedback_type=payload["feedback_type"],
            feedback_actor_kind=payload.get("feedback_actor_kind"),
            feedback_actor_id=payload.get("feedback_actor_id"),
            feedback_payload=json.dumps(payload.get("feedback_payload", {}), ensure_ascii=False),
        )
        self.session.add(model)
        self.session.flush()
        return model
