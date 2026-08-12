import json
from pathlib import Path


def test_golden_replay_fixture_has_required_core_fields() -> None:
    fixture_path = Path(__file__).resolve().parents[1] / "fixtures" / "replay_session.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "1.0"
    assert payload["session"]["tenant_id"] == "tenant-a"
    assert payload["events"][0]["event_id"] == "evt-001"
