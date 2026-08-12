from __future__ import annotations

from fastapi.testclient import TestClient

from edu_cs_core.api.app import create_app
from edu_cs_core.services.replay_processor import ReplayProcessor
from edu_cs_core.storage.database import SessionLocal


def test_feedback_api_attaches_feedback_to_evaluation_and_source(replay_payload: dict) -> None:
    processor = ReplayProcessor(SessionLocal)
    processor.process(replay_payload)

    client = TestClient(create_app())
    response = client.post(
        "/api/feedback",
        json={
            "session_id": "replay-001",
            "evaluation_id": "replay-001:route",
            "attribution_id": "replay-001:route:primary",
            "feedback_type": "corrected",
            "feedback_actor_kind": "reviewer",
            "feedback_actor_id": "qa-001",
            "feedback_payload": {"note": "路由需要人工复核"},
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["session_id"] == "replay-001"
    assert payload["evaluation_id"] == "replay-001:route"
    assert payload["attribution_id"] == "replay-001:route:primary"
    assert payload["feedback_type"] == "corrected"
    assert payload["feedback_payload"]["note"] == "路由需要人工复核"
