from __future__ import annotations

from edu_cs_core.services.replay_processor import ReplayProcessor
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.models import FeedbackRecordModel


def test_feedback_persists_with_session_evaluation_and_attribution_links(replay_payload: dict) -> None:
    processor = ReplayProcessor(SessionLocal)
    processor.process(replay_payload)

    from edu_cs_core.services.feedback_service import FeedbackService

    service = FeedbackService(SessionLocal)
    result = service.add_feedback(
        {
            "session_id": "replay-001",
            "evaluation_id": "replay-001:route",
            "attribution_id": "replay-001:route:primary",
            "feedback_type": "corrected",
            "feedback_actor_kind": "reviewer",
            "feedback_actor_id": "qa-001",
            "feedback_payload": {"note": "保留反馈链路"},
        }
    )

    assert result["feedback_type"] == "corrected"

    with SessionLocal() as session:
        records = session.query(FeedbackRecordModel).all()

    assert len(records) == 1
    assert records[0].session_id == "replay-001"
    assert records[0].evaluation_id == "replay-001:route"
    assert records[0].attribution_id == "replay-001:route:primary"
