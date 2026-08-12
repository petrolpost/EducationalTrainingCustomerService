from __future__ import annotations

from edu_cs_core.services.logging import get_logger, log_event
from edu_cs_core.services.query_scope_service import QueryScopeService
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.models import ReplaySessionModel


logger = get_logger(__name__)


class ReviewAggregateService:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory
        self._scope_service = QueryScopeService(session_factory)

    def list_sessions(self, *, principal_id: str, role_template_key: str, tenant_id: str, school_id: str | None = None) -> list[ReplaySessionModel]:
        scope = self._scope_service.resolve(
            principal_id=principal_id,
            role_template_key=role_template_key,
            tenant_id=tenant_id,
            school_id=school_id,
        )
        with self._session_factory() as session:
            query = session.query(ReplaySessionModel).filter(ReplaySessionModel.tenant_id == scope.tenant_id)
            if scope.school_ids:
                query = query.filter(ReplaySessionModel.school_id.in_(scope.school_ids))
            sessions = query.order_by(ReplaySessionModel.session_id.asc()).all()
        log_event(
            logger,
            "review.sessions.listed",
            principal_id=principal_id,
            role_template_key=role_template_key,
            tenant_id=tenant_id,
            school_id=school_id,
            scope_school_ids=sorted(scope.school_ids),
            session_count=len(sessions),
        )
        return sessions

    def aggregate(self, **kwargs) -> dict:
        sessions = self.list_sessions(**kwargs)
        aggregate = {
            "session_count": len(sessions),
            "completed_count": sum(1 for session in sessions if session.status == "completed"),
        }
        log_event(logger, "review.aggregate.generated", **kwargs, **aggregate)
        return aggregate
