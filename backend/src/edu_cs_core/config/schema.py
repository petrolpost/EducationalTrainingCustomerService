from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SignalPolicyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    default_consumption_tier: str = "observe"
    lifecycle_state: str = "experimental"


class BaselineConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    config_version: str
    spec_version: str
    route_defaults: dict[str, Any] = Field(default_factory=dict)
    signal_policies: dict[str, SignalPolicyConfig] = Field(default_factory=dict)
    scope_defaults: dict[str, Any] = Field(default_factory=dict)
