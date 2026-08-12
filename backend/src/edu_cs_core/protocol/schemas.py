from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ReplaySessionInput(BaseModel):
    session_id: str
    tenant_id: str
    school_id: str | None = None
    source_kind: str


class ReplayEventInput(BaseModel):
    event_id: str
    seq: int
    occurred_at: datetime
    event_type: str
    actor_kind: str
    actor_id: str | None = None
    content: str | None = None
    channel: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    extensions: dict[str, Any] = Field(default_factory=dict)


class ReplayRequest(BaseModel):
    schema_version: str
    session: ReplaySessionInput
    events: list[ReplayEventInput]


class SourceSummary(BaseModel):
    source_type: str
    source_ref: str
    source_version: str | None = None
    contribution_kind: str | None = None


class EvaluationOutput(BaseModel):
    evaluation_id: str
    evaluation_kind: str
    label: str
    signal_key: str | None = None
    signal_config_version: str | None = None
    consumption_tier_snapshot: str | None = None
    lifecycle_state_snapshot: str | None = None
    value: dict[str, Any]
    primary_source: SourceSummary
    contributing_sources: list[SourceSummary] = Field(default_factory=list)


class ReplayResult(BaseModel):
    schema_version: str = "1.0"
    session_id: str
    status: str
    route: dict[str, Any]
    evaluations: list[EvaluationOutput]


class ReplayTimeline(BaseModel):
    session_id: str
    status: str
    events: list[dict[str, Any]]
    evaluations: list[dict[str, Any]]
