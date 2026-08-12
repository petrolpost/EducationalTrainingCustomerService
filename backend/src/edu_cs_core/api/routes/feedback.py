from __future__ import annotations

from fastapi import APIRouter, HTTPException

from edu_cs_core.services.feedback_service import FeedbackService


router = APIRouter(prefix="/api/feedback", tags=["feedback"])
service = FeedbackService()


@router.post("", status_code=201)
async def add_feedback(payload: dict) -> dict:
    try:
        return service.add_feedback(payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Replay session not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
