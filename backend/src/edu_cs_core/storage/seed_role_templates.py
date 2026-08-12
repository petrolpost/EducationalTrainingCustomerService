from __future__ import annotations

from edu_cs_core.domain.enums import ReadMode, RoleTemplateKey, ScopeLevel
from edu_cs_core.storage.models import RoleTemplateModel


DEFAULT_ROLE_TEMPLATES = [
    {
        "role_template_key": RoleTemplateKey.SEAT_SCHOOL.value,
        "scope_level": ScopeLevel.SCHOOL.value,
        "read_mode": ReadMode.SCOPED_OPERATE.value,
        "can_cross_school": False,
        "can_cross_tenant": False,
        "requires_explicit_grant": False,
    },
    {
        "role_template_key": RoleTemplateKey.SCHOOL_MANAGER.value,
        "scope_level": ScopeLevel.SCHOOL.value,
        "read_mode": ReadMode.SCOPED_OPERATE.value,
        "can_cross_school": False,
        "can_cross_tenant": False,
        "requires_explicit_grant": False,
    },
    {
        "role_template_key": RoleTemplateKey.TENANT_MANAGER.value,
        "scope_level": ScopeLevel.TENANT.value,
        "read_mode": ReadMode.SCOPED_OPERATE.value,
        "can_cross_school": True,
        "can_cross_tenant": False,
        "requires_explicit_grant": False,
    },
    {
        "role_template_key": RoleTemplateKey.PLATFORM_AUDITOR.value,
        "scope_level": ScopeLevel.EXPLICIT_GRANT.value,
        "read_mode": ReadMode.READ_ONLY.value,
        "can_cross_school": True,
        "can_cross_tenant": True,
        "requires_explicit_grant": True,
    },
]


def seed_role_templates(session_factory) -> None:
    with session_factory() as session:
        for template in DEFAULT_ROLE_TEMPLATES:
            session.merge(RoleTemplateModel(**template))
        session.commit()
