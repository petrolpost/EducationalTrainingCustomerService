from __future__ import annotations

import typer

from edu_cs_core.cli.config import app as config_app
from edu_cs_core.cli.replay import app as replay_app
from edu_cs_core.cli.review import app as review_app
from edu_cs_core.cli.signals import app as signals_app
from edu_cs_core.storage.bootstrap import bootstrap_database


app = typer.Typer(help="Educational training customer service core CLI")
app.add_typer(config_app, name="config")
app.add_typer(replay_app, name="replay")
app.add_typer(review_app, name="review")
app.add_typer(signals_app, name="signals")


@app.callback()
def main() -> None:
    """CLI entrypoint."""


@app.command("bootstrap-db")
def bootstrap_db() -> None:
    """Create local SQLite tables."""
    bootstrap_database()
    typer.echo("database bootstrapped")
