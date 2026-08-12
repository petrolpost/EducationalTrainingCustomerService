from __future__ import annotations

import json
from pathlib import Path

import typer

from edu_cs_core.config.service import ConfigService


app = typer.Typer(help="Baseline configuration commands")
service = ConfigService()


@app.command("validate")
def validate(input: Path = typer.Option(...)) -> None:
    service.validate_file(input)
    typer.echo("valid")


@app.command("diff")
def diff(left: Path = typer.Option(...), right: Path = typer.Option(...), output: str = typer.Option("human")) -> None:
    result = service.diff_files(left, right)
    if output == "json":
        typer.echo(json.dumps(result, ensure_ascii=False))
        return
    typer.echo(f"changed={result['changed']}")
