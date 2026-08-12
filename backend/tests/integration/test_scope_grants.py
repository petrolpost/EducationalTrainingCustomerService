from __future__ import annotations

from edu_cs_core.services.query_scope_service import QueryScopeService
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.seed_role_templates import seed_role_templates


def test_explicit_grants_expand_scope_for_read_only_auditor() -> None:
    seed_role_templates(SessionLocal)
    service = QueryScopeService(SessionLocal)

    service.grant_scope(
        principal_id="auditor-1",
        role_template_key="platform_auditor",
        tenant_id="tenant-a",
        school_id="school-01",
        grant_scope="school",
        granted_by="system",
    )

    scope = service.resolve(
        principal_id="auditor-1",
        role_template_key="platform_auditor",
        tenant_id="tenant-a",
    )

    assert scope.read_only is True
    assert "school-01" in scope.school_ids
