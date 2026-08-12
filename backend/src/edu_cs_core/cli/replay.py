from __future__ import annotations

import json
from pathlib import Path

import typer

from edu_cs_core.services.replay_processor import ReplayProcessor


app = typer.Typer(help="Replay processing commands")
processor = ReplayProcessor()


@app.command("run")
def replay_run(input: Path = typer.Option(...), output: str = typer.Option("human")) -> None:
    payload = json.loads(input.read_text(encoding="utf-8"))
    result = processor.process(payload)
    if output == "json":
        typer.echo(result.model_dump_json())
        return
    typer.echo(f"{result.session_id} {result.status} {result.route['label']}")


@app.command("show")
def replay_show(session: str = typer.Option(...), output: str = typer.Option("human")) -> None:
    result = processor.get_summary(session)
    if output == "json":
        typer.echo(json.dumps(result, ensure_ascii=False))
        return
    typer.echo(f"{result['session_id']} {result['status']}")


@app.command("timeline")
def replay_timeline(session: str = typer.Option(...), output: str = typer.Option("human")) -> None:
    result = processor.get_timeline(session)
    if output == "json":
        typer.echo(result.model_dump_json())
        return
    typer.echo(f"{result.session_id} events={len(result.events)} evaluations={len(result.evaluations)}")
