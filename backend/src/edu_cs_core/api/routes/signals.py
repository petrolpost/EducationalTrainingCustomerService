from __future__ import annotations

from fastapi import APIRouter, HTTPException

from edu_cs_core.governance.lifecycle_service import SignalLifecycleService
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.signal_repository import SignalRepository


router = APIRouter(prefix="/api/signals", tags=["signals"])
service = SignalLifecycleService(SessionLocal)


@router.get("/{signal_key}")
async def get_signal_profile(signal_key: str) -> dict:
    with SessionLocal() as session:
        repository = SignalRepository(session)
        profile = repository.get_profile(signal_key)
        if profile is None:
            raise HTTPException(status_code=404, detail="Signal profile not found")
        return {
            "signal_key": profile.signal_key,
            "display_name": profile.display_name,
            "default_consumption_tier": profile.default_consumption_tier,
            "lifecycle_state": profile.lifecycle_state,
            "current_config_version": profile.current_config_version,
        }


@router.post("/{signal_key}/lifecycle-events", status_code=202)
async def create_signal_lifecycle_event(signal_key: str, payload: dict) -> dict:
    try:
        service.record_event(signal_key=signal_key, **payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Signal profile not found") from exc
    return {"signal_key": signal_key, "accepted": True}
