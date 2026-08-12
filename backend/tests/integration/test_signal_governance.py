from __future__ import annotations

from edu_cs_core.governance.lifecycle_service import SignalLifecycleService
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.models import SignalLifecycleEventModel, SignalProfileModel


def test_signal_lifecycle_event_updates_profile_state() -> None:
    service = SignalLifecycleService(SessionLocal)

    service.ensure_profile("attention_shift", "Attention Shift")
    service.record_event(
        signal_key="attention_shift",
        signal_config_version="0.2.0",
        governance_tier="major",
        change_type="upgrade",
        from_lifecycle_state="experimental",
        to_lifecycle_state="validated",
        from_consumption_tier="observe",
        to_consumption_tier="prompt",
        validation_report_ref="report://attention/001",
        approved_by="qa-reviewer",
    )

    with SessionLocal() as session:
        profile = session.get(SignalProfileModel, "attention_shift")
        events = session.query(SignalLifecycleEventModel).all()

    assert profile is not None
    assert profile.lifecycle_state == "validated"
    assert profile.default_consumption_tier == "prompt"
    assert profile.current_config_version == "0.2.0"
    assert len(events) == 1
