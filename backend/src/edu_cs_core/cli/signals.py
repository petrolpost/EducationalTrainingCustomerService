from __future__ import annotations

import json

import typer

from edu_cs_core.governance.lifecycle_service import SignalLifecycleService
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.signal_repository import SignalRepository


app = typer.Typer(help="Signal governance commands")
service = SignalLifecycleService(SessionLocal)


@app.command("ensure-profile")
def ensure_profile(signal_key: str, display_name: str) -> None:
    service.ensure_profile(signal_key, display_name)
    typer.echo(f"ensured {signal_key}")


@app.command("show-profile")
def show_profile(signal_key: str, output: str = typer.Option("human")) -> None:
    with SessionLocal() as session:
        repository = SignalRepository(session)
        profile = repository.get_profile(signal_key)
        if profile is None:
            raise typer.Exit(code=1)
        payload = {
            "signal_key": profile.signal_key,
            "display_name": profile.display_name,
            "default_consumption_tier": profile.default_consumption_tier,
            "lifecycle_state": profile.lifecycle_state,
            "current_config_version": profile.current_config_version,
        }
    if output == "json":
        typer.echo(json.dumps(payload, ensure_ascii=False))
        return
    typer.echo(f"{payload['signal_key']} {payload['lifecycle_state']} {payload['default_consumption_tier']}")
