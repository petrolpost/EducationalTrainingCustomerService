from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from edu_cs_core.cli.main import app


runner = CliRunner()


def test_config_validate_and_diff_commands(tmp_path: Path) -> None:
    left = tmp_path / "baseline-a.json"
    right = tmp_path / "baseline-b.json"
    left.write_text(
        json.dumps(
            {
                "config_version": "0.1.0",
                "spec_version": "001-edu-cs-core",
                "signal_policies": {"attention_shift": {"default_consumption_tier": "observe", "lifecycle_state": "experimental"}},
            }
        ),
        encoding="utf-8",
    )
    right.write_text(
        json.dumps(
            {
                "config_version": "0.2.0",
                "spec_version": "001-edu-cs-core",
                "signal_policies": {"attention_shift": {"default_consumption_tier": "prompt", "lifecycle_state": "validated"}},
            }
        ),
        encoding="utf-8",
    )

    validate_result = runner.invoke(app, ["config", "validate", "--input", str(left)])
    diff_result = runner.invoke(app, ["config", "diff", "--left", str(left), "--right", str(right), "--output", "json"])

    assert validate_result.exit_code == 0
    assert "valid" in validate_result.stdout
    assert diff_result.exit_code == 0
    diff_payload = json.loads(diff_result.stdout)
    assert diff_payload["changed"] is True
