from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from edu_cs_core.config.service import ConfigService


router = APIRouter(prefix="/api/config", tags=["config"])
service = ConfigService()


@router.post("/validate")
async def validate_config(payload: dict) -> dict:
    temp_path = Path("backend/.data/config-validate.json")
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_text(__import__("json").dumps(payload), encoding="utf-8")
    model = service.validate_file(temp_path)
    return {"config_version": model.config_version, "valid": True}
