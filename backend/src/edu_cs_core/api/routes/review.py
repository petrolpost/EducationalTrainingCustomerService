from __future__ import annotations

from fastapi import APIRouter, Header

from edu_cs_core.services.review_aggregate_service import ReviewAggregateService


router = APIRouter(prefix="/api/review", tags=["review"])
service = ReviewAggregateService()


def _context(
    principal_id: str | None,
    role_template: str | None,
    tenant_id: str | None,
    school_id: str | None,
) -> dict:
    return {
        "principal_id": principal_id or "anonymous",
        "role_template_key": role_template or "seat_school",
        "tenant_id": tenant_id or "tenant-a",
        "school_id": school_id,
    }


@router.get("/replays")
async def list_replays(
    x_principal_id: str | None = Header(default=None),
    x_role_template: str | None = Header(default=None),
    x_tenant_id: str | None = Header(default=None),
    x_school_id: str | None = Header(default=None),
) -> dict:
    items = service.list_sessions(**_context(x_principal_id, x_role_template, x_tenant_id, x_school_id))
    return {
        "items": [
            {
                "session_id": item.session_id,
                "tenant_id": item.tenant_id,
                "school_id": item.school_id,
                "status": item.status,
            }
            for item in items
        ]
    }


@router.get("/aggregate")
async def review_aggregate(
    x_principal_id: str | None = Header(default=None),
    x_role_template: str | None = Header(default=None),
    x_tenant_id: str | None = Header(default=None),
    x_school_id: str | None = Header(default=None),
) -> dict:
    return service.aggregate(**_context(x_principal_id, x_role_template, x_tenant_id, x_school_id))
