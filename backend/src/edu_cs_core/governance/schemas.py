from __future__ import annotations

from pydantic import BaseModel


class SignalPolicySnapshot(BaseModel):
    signal_key: str
    signal_config_version: str
    consumption_tier_snapshot: str
    lifecycle_state_snapshot: str


class SignalLifecycleChange(BaseModel):
    signal_key: str
    signal_config_version: str
    governance_tier: str
    change_type: str
    from_lifecycle_state: str | None = None
    to_lifecycle_state: str | None = None
    from_consumption_tier: str | None = None
    to_consumption_tier: str | None = None
    validation_report_ref: str | None = None
    approved_by: str | None = None
