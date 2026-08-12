from __future__ import annotations

from edu_cs_core.services.replay_processor import ReplayProcessor
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.models import AttributionRecordModel, EvaluationRecordModel, ReplaySessionModel


def test_replay_processor_persists_session_evaluations_and_attributions(replay_payload: dict) -> None:
    processor = ReplayProcessor(SessionLocal)

    result = processor.process(replay_payload)

    assert result.session_id == "replay-001"
    assert result.status == "completed"

    with SessionLocal() as session:
        stored_session = session.get(ReplaySessionModel, "replay-001")
        evaluations = session.query(EvaluationRecordModel).all()
        attributions = session.query(AttributionRecordModel).all()

    assert stored_session is not None
    assert len(evaluations) >= 1
    assert len(attributions) >= 1
