from __future__ import annotations

from dataclasses import dataclass, field

from edu_cs_core.domain.enums import RoleTemplateKey


@dataclass(slots=True)
class ScopeContext:
    principal_id: str
    role_template: RoleTemplateKey
    tenant_id: str
    school_ids: set[str] = field(default_factory=set)
    explicit_grants: set[str] = field(default_factory=set)


@dataclass(slots=True)
class ResolvedScope:
    tenant_id: str
    school_ids: set[str]
    read_only: bool


def resolve_scope(context: ScopeContext) -> ResolvedScope:
    read_only = context.role_template is RoleTemplateKey.PLATFORM_AUDITOR
    return ResolvedScope(
        tenant_id=context.tenant_id,
        school_ids=set(context.school_ids),
        read_only=read_only,
    )
