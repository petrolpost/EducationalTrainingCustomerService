from __future__ import annotations

from enum import StrEnum


class ReplayStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SourceKind(StrEnum):
    SIMULATED = "simulated"
    IMPORTED = "imported"
    HISTORICAL = "historical"


class EvaluationKind(StrEnum):
    ROUTE = "route"
    SIGNAL = "signal"
    RISK = "risk"
    SUMMARY = "summary"
    ACTION_RECOMMENDATION = "action_recommendation"


class ConsumptionTier(StrEnum):
    OBSERVE = "observe"
    PROMPT = "prompt"
    DECISION = "decision"


class LifecycleState(StrEnum):
    EXPERIMENTAL = "experimental"
    VALIDATED = "validated"
    FROZEN = "frozen"
    RETIRED = "retired"


class AttributionSourceRole(StrEnum):
    PRIMARY = "primary"
    CONTRIBUTING = "contributing"


class ContributionKind(StrEnum):
    TRIGGER = "trigger"
    SUPPORT = "support"
    VERIFY = "verify"
    OVERRIDE = "override"


class SourceType(StrEnum):
    RAG = "rag"
    RULE = "rule"
    MODEL = "model"
    HUMAN = "human"


class RoleTemplateKey(StrEnum):
    SEAT_SCHOOL = "seat_school"
    SCHOOL_MANAGER = "school_manager"
    TENANT_MANAGER = "tenant_manager"
    PLATFORM_AUDITOR = "platform_auditor"


class ScopeLevel(StrEnum):
    SELF = "self"
    SCHOOL = "school"
    TENANT = "tenant"
    EXPLICIT_GRANT = "explicit_grant"


class ReadMode(StrEnum):
    READ_ONLY = "read_only"
    SCOPED_OPERATE = "scoped_operate"
