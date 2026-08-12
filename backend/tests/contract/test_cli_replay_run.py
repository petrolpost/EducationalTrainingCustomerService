from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from edu_cs_core.cli.main import app


runner = CliRunner()


def test_replay_run_command_processes_fixture(tmp_path: Path, replay_payload: dict) -> None:
    input_path = tmp_path / "replay.json"
    input_path.write_text(json.dumps(replay_payload), encoding="utf-8")

    result = runner.invoke(app, ["replay", "run", "--input", str(input_path), "--output", "json"])

    assert result.exit_code == 0
    output = json.loads(result.stdout)
    assert output["session_id"] == "replay-001"
    assert output["status"] == "completed"
    assert output["route"]["label"] == "in_service.leave_consultation"
    assert any(item["evaluation_kind"] == "action_recommendation" for item in output["evaluations"])
    assert any(item["evaluation_kind"] == "risk" for item in output["evaluations"])


def test_replay_show_and_timeline_commands_read_processed_session(tmp_path: Path, replay_payload: dict) -> None:
    input_path = tmp_path / "replay.json"
    input_path.write_text(json.dumps(replay_payload), encoding="utf-8")

    run_result = runner.invoke(app, ["replay", "run", "--input", str(input_path)])
    assert run_result.exit_code == 0

    show_result = runner.invoke(app, ["replay", "show", "--session", "replay-001", "--output", "json"])
    timeline_result = runner.invoke(app, ["replay", "timeline", "--session", "replay-001", "--output", "json"])

    assert show_result.exit_code == 0
    assert timeline_result.exit_code == 0
    assert json.loads(show_result.stdout)["session_id"] == "replay-001"
    timeline = json.loads(timeline_result.stdout)
    assert timeline["session_id"] == "replay-001"
    assert len(timeline["events"]) == 1
    assert len(timeline["evaluations"]) >= 1
    assert any(item["evaluation_kind"] == "action_recommendation" for item in timeline["evaluations"])
    assert any(item["evaluation_kind"] == "risk" for item in timeline["evaluations"])
