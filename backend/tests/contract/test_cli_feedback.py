from __future__ import annotations

import json

from typer.testing import CliRunner

from edu_cs_core.cli.main import app
from edu_cs_core.services.replay_processor import ReplayProcessor
from edu_cs_core.storage.database import SessionLocal


runner = CliRunner()


def test_review_feedback_add_command_records_feedback(replay_payload: dict) -> None:
    processor = ReplayProcessor(SessionLocal)
    processor.process(replay_payload)

    result = runner.invoke(
        app,
        [
            "review",
            "feedback",
            "add",
            "--session-id",
            "replay-001",
            "--evaluation-id",
            "replay-001:route",
            "--attribution-id",
            "replay-001:route:primary",
            "--feedback-type",
            "corrected",
            "--actor-kind",
            "reviewer",
            "--actor-id",
            "qa-001",
            "--payload",
            '{"note":"来源需要补充说明"}',
            "--output",
            "json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["session_id"] == "replay-001"
    assert payload["evaluation_id"] == "replay-001:route"
    assert payload["attribution_id"] == "replay-001:route:primary"
    assert payload["feedback_payload"]["note"] == "来源需要补充说明"
