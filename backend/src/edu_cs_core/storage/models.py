from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edu_cs_core.storage.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ReplaySessionModel(Base):
    __tablename__ = "replay_sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    protocol_version: Mapped[str] = mapped_column(String(16), default="1.0")
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    school_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    source_kind: Mapped[str] = mapped_column(String(32), default="simulated")
    event_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    events: Mapped[list["ConversationEventModel"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    evaluations: Mapped[list["EvaluationRecordModel"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    feedback_records: Mapped[list["FeedbackRecordModel"]] = relationship(back_populates="session", cascade="all, delete-orphan")


class ConversationEventModel(Base):
    __tablename__ = "conversation_events"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("replay_sessions.session_id"), index=True)
    seq: Mapped[int] = mapped_column(Integer)
    occurred_at: Mapped[datetime] = mapped_column(DateTime)
    event_type: Mapped[str] = mapped_column(String(32))
    actor_kind: Mapped[str] = mapped_column(String(32))
    actor_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    channel: Mapped[str | None] = mapped_column(String(32), nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")
    extension_json: Mapped[str] = mapped_column(Text, default="{}")

    session: Mapped["ReplaySessionModel"] = relationship(back_populates="events")


class SignalProfileModel(Base):
    __tablename__ = "signal_profiles"

    signal_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(128))
    default_consumption_tier: Mapped[str] = mapped_column(String(32))
    lifecycle_state: Mapped[str] = mapped_column(String(32))
    current_config_version: Mapped[str] = mapped_column(String(32), default="0.1.0")

    evaluations: Mapped[list["EvaluationRecordModel"]] = relationship(back_populates="signal_profile")
    lifecycle_events: Mapped[list["SignalLifecycleEventModel"]] = relationship(back_populates="signal_profile")


class EvaluationRecordModel(Base):
    __tablename__ = "evaluation_records"

    evaluation_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("replay_sessions.session_id"), index=True)
    event_id: Mapped[str | None] = mapped_column(ForeignKey("conversation_events.event_id"), nullable=True, index=True)
    evaluation_kind: Mapped[str] = mapped_column(String(64), index=True)
    label: Mapped[str] = mapped_column(String(128), index=True)
    signal_key: Mapped[str | None] = mapped_column(ForeignKey("signal_profiles.signal_key"), nullable=True, index=True)
    value_json: Mapped[str] = mapped_column(Text, default="{}")
    signal_config_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    consumption_tier_snapshot: Mapped[str | None] = mapped_column(String(32), nullable=True)
    lifecycle_state_snapshot: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confidence: Mapped[str | None] = mapped_column(String(16), nullable=True)
    produced_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    rule_or_model_revision: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_primary_for_session_state: Mapped[bool] = mapped_column(Boolean, default=False)

    session: Mapped["ReplaySessionModel"] = relationship(back_populates="evaluations")
    signal_profile: Mapped[Optional["SignalProfileModel"]] = relationship(back_populates="evaluations")
    attributions: Mapped[list["AttributionRecordModel"]] = relationship(back_populates="evaluation", cascade="all, delete-orphan")


class AttributionRecordModel(Base):
    __tablename__ = "attribution_records"

    attribution_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    evaluation_id: Mapped[str] = mapped_column(ForeignKey("evaluation_records.evaluation_id"), index=True)
    source_role: Mapped[str] = mapped_column(String(32))
    contribution_kind: Mapped[str] = mapped_column(String(32))
    source_type: Mapped[str] = mapped_column(String(32))
    source_ref: Mapped[str] = mapped_column(String(128))
    source_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    evidence_excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    evidence_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    evaluation: Mapped["EvaluationRecordModel"] = relationship(back_populates="attributions")


class BaselineConfigModel(Base):
    __tablename__ = "baseline_configs"

    config_version: Mapped[str] = mapped_column(String(32), primary_key=True)
    spec_version: Mapped[str] = mapped_column(String(64))
    change_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    rollback_target: Mapped[str | None] = mapped_column(String(32), nullable=True)
    schema_version: Mapped[str] = mapped_column(String(32))
    config_payload: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class FeedbackRecordModel(Base):
    __tablename__ = "feedback_records"

    feedback_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("replay_sessions.session_id"), index=True)
    evaluation_id: Mapped[str | None] = mapped_column(ForeignKey("evaluation_records.evaluation_id"), nullable=True, index=True)
    attribution_id: Mapped[str | None] = mapped_column(ForeignKey("attribution_records.attribution_id"), nullable=True, index=True)
    feedback_type: Mapped[str] = mapped_column(String(32))
    feedback_actor_kind: Mapped[str | None] = mapped_column(String(32), nullable=True)
    feedback_actor_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    feedback_payload: Mapped[str] = mapped_column(Text, default="{}")
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    session: Mapped["ReplaySessionModel"] = relationship(back_populates="feedback_records")


class SignalLifecycleEventModel(Base):
    __tablename__ = "signal_lifecycle_events"

    lifecycle_event_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    signal_key: Mapped[str] = mapped_column(ForeignKey("signal_profiles.signal_key"), index=True)
    signal_config_version: Mapped[str] = mapped_column(String(32))
    governance_tier: Mapped[str] = mapped_column(String(16))
    change_type: Mapped[str] = mapped_column(String(32))
    from_lifecycle_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    to_lifecycle_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    from_consumption_tier: Mapped[str | None] = mapped_column(String(32), nullable=True)
    to_consumption_tier: Mapped[str | None] = mapped_column(String(32), nullable=True)
    validation_report_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    decision_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    signal_profile: Mapped["SignalProfileModel"] = relationship(back_populates="lifecycle_events")


class RoleTemplateModel(Base):
    __tablename__ = "role_templates"

    role_template_key: Mapped[str] = mapped_column(String(64), primary_key=True)
    scope_level: Mapped[str] = mapped_column(String(32))
    read_mode: Mapped[str] = mapped_column(String(32))
    can_cross_school: Mapped[bool] = mapped_column(Boolean, default=False)
    can_cross_tenant: Mapped[bool] = mapped_column(Boolean, default=False)
    requires_explicit_grant: Mapped[bool] = mapped_column(Boolean, default=True)


class ScopeGrantModel(Base):
    __tablename__ = "scope_grants"

    grant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    principal_id: Mapped[str] = mapped_column(String(64), index=True)
    role_template_key: Mapped[str] = mapped_column(ForeignKey("role_templates.role_template_key"))
    tenant_id: Mapped[str] = mapped_column(String(64), index=True)
    school_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    grant_scope: Mapped[str] = mapped_column(String(64))
    granted_by: Mapped[str] = mapped_column(String(64))
    granted_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
