from __future__ import annotations

from fastapi.testclient import TestClient

from edu_cs_core.api.app import create_app


def test_replay_api_creates_and_reads_replay_session(replay_payload: dict) -> None:
    client = TestClient(create_app())

    create_response = client.post("/api/replays", json=replay_payload)
    assert create_response.status_code == 202
    assert create_response.json()["session_id"] == "replay-001"

    show_response = client.get("/api/replays/replay-001")
    timeline_response = client.get("/api/replays/replay-001/timeline")

    assert show_response.status_code == 200
    assert timeline_response.status_code == 200
    assert show_response.json()["status"] == "completed"
    assert timeline_response.json()["session_id"] == "replay-001"
    assert len(timeline_response.json()["evaluations"]) >= 1
    assert any(item["evaluation_kind"] == "action_recommendation" for item in timeline_response.json()["evaluations"])
    assert any(item["evaluation_kind"] == "risk" for item in timeline_response.json()["evaluations"])
