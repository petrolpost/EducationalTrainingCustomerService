from __future__ import annotations

from dataclasses import dataclass
import logging
from uuid import uuid4

from edu_cs_core.domain.enums import RoleTemplateKey
from edu_cs_core.services.logging import get_logger, log_event
from edu_cs_core.services.scope_resolver import ResolvedScope
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.models import RoleTemplateModel, ScopeGrantModel


logger = get_logger(__name__)


@dataclass(slots=True)
class ScopeRequest:
    principal_id: str
    role_template_key: str
    tenant_id: str
    school_id: str | None = None


class QueryScopeService:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory

    def grant_scope(
        self,
        *,
        principal_id: str,
        role_template_key: str,
        tenant_id: str,
        school_id: str | None,
        grant_scope: str,
        granted_by: str,
    ) -> None:
        with self._session_factory() as session:
            session.add(
                ScopeGrantModel(
                    grant_id=str(uuid4()),
                    principal_id=principal_id,
                    role_template_key=role_template_key,
                    tenant_id=tenant_id,
                    school_id=school_id,
                    grant_scope=grant_scope,
                    granted_by=granted_by,
                )
            )
            session.commit()
        log_event(
            logger,
            "review.scope.granted",
            principal_id=principal_id,
            role_template_key=role_template_key,
            tenant_id=tenant_id,
            school_id=school_id,
            grant_scope=grant_scope,
            granted_by=granted_by,
        )

    def resolve(self, *, principal_id: str, role_template_key: str, tenant_id: str, school_id: str | None = None) -> ResolvedScope:
        with self._session_factory() as session:
            template = session.get(RoleTemplateModel, role_template_key)
            if template is None:
                log_event(
                    logger,
                    "review.scope.template_missing",
                    level=logging.ERROR,
                    principal_id=principal_id,
                    role_template_key=role_template_key,
                    tenant_id=tenant_id,
                )
                raise KeyError(role_template_key)
            grants = (
                session.query(ScopeGrantModel)
                .filter(
                    ScopeGrantModel.principal_id == principal_id,
                    ScopeGrantModel.role_template_key == role_template_key,
                    ScopeGrantModel.tenant_id == tenant_id,
                )
                .all()
            )
            school_ids = {grant.school_id for grant in grants if grant.school_id}
            if role_template_key == RoleTemplateKey.TENANT_MANAGER.value:
                school_ids = set()
            elif school_id and not school_ids:
                school_ids = {school_id}
            resolved = ResolvedScope(
                tenant_id=tenant_id,
                school_ids=school_ids,
                read_only=template.read_mode == "read_only",
            )
            log_event(
                logger,
                "review.scope.resolved",
                principal_id=principal_id,
                role_template_key=role_template_key,
                tenant_id=tenant_id,
                requested_school_id=school_id,
                school_ids=sorted(resolved.school_ids),
                read_only=resolved.read_only,
                grant_count=len(grants),
            )
            return resolved
