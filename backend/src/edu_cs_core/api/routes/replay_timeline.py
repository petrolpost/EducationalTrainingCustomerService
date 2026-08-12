from __future__ import annotations

from fastapi import APIRouter, HTTPException

from edu_cs_core.api.serializers.replay import serialize_replay_timeline
from edu_cs_core.services.replay_processor import ReplayProcessor


router = APIRouter(prefix="/api/replays", tags=["replays"])
processor = ReplayProcessor()


@router.get("/{session_id}/timeline")
async def replay_timeline(session_id: str) -> dict:
    try:
        return serialize_replay_timeline(processor.get_timeline(session_id))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Replay not found") from exc
