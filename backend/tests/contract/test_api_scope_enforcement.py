from __future__ import annotations

from fastapi.testclient import TestClient

from edu_cs_core.api.app import create_app
from edu_cs_core.services.replay_processor import ReplayProcessor
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.seed_role_templates import seed_role_templates


def test_review_routes_apply_least_visibility_scope(replay_payload: dict) -> None:
    processor = ReplayProcessor(SessionLocal)
    seed_role_templates(SessionLocal)

    payload_a = replay_payload
    payload_b = {
        **replay_payload,
        "session": {
            **replay_payload["session"],
            "session_id": "replay-002",
            "tenant_id": "tenant-b",
            "school_id": "school-02",
        },
        "events": [
            {
                **replay_payload["events"][0],
                "event_id": "evt-002",
            }
        ],
    }
    processor.process(payload_a)
    processor.process(payload_b)

    client = TestClient(create_app())
    headers = {
        "x-principal-id": "tenant-manager-a",
        "x-role-template": "tenant_manager",
        "x-tenant-id": "tenant-a",
    }

    list_response = client.get("/api/review/replays", headers=headers)
    aggregate_response = client.get("/api/review/aggregate", headers=headers)

    assert list_response.status_code == 200
    assert aggregate_response.status_code == 200
    assert [item["session_id"] for item in list_response.json()["items"]] == ["replay-001"]
    assert aggregate_response.json()["session_count"] == 1
