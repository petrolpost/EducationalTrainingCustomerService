from __future__ import annotations

from fastapi import APIRouter, HTTPException

from edu_cs_core.api.serializers.replay import serialize_replay_result
from edu_cs_core.services.replay_processor import ReplayProcessor


router = APIRouter(prefix="/api/replays", tags=["replays"])
processor = ReplayProcessor()


@router.post("", status_code=202)
async def create_replay(payload: dict) -> dict:
    result = processor.process(payload)
    return serialize_replay_result(result)


@router.get("/{session_id}")
async def show_replay(session_id: str) -> dict:
    try:
        return processor.get_summary(session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Replay not found") from exc
