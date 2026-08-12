from __future__ import annotations

from edu_cs_core.services.replay_processor import ReplayProcessor


def test_replay_output_contains_governed_signal_snapshots(replay_payload: dict, session_factory) -> None:
    processor = ReplayProcessor(session_factory)

    result = processor.process(replay_payload)

    signal_evaluations = [evaluation for evaluation in result.evaluations if evaluation.evaluation_kind == "signal"]
    assert len(signal_evaluations) == 1
    signal = signal_evaluations[0]
    assert signal.signal_key == "attention_shift"
    assert signal.signal_config_version == "0.1.0"
    assert signal.consumption_tier_snapshot == "observe"
    assert signal.lifecycle_state_snapshot == "experimental"
