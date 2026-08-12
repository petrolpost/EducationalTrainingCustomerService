from __future__ import annotations

import json

import typer

from edu_cs_core.services.feedback_service import FeedbackService


app = typer.Typer(help="Review workflow commands")
feedback_app = typer.Typer(help="Feedback commands")
app.add_typer(feedback_app, name="feedback")
service = FeedbackService()


@feedback_app.command("add")
def add_feedback(
    session_id: str = typer.Option(...),
    evaluation_id: str | None = typer.Option(default=None),
    attribution_id: str | None = typer.Option(default=None),
    feedback_type: str = typer.Option(...),
    actor_kind: str | None = typer.Option(default=None),
    actor_id: str | None = typer.Option(default=None),
    payload: str = typer.Option("{}"),
    output: str = typer.Option("human"),
) -> None:
    try:
        feedback_payload = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter("payload must be valid JSON") from exc

    result = service.add_feedback(
        {
            "session_id": session_id,
            "evaluation_id": evaluation_id,
            "attribution_id": attribution_id,
            "feedback_type": feedback_type,
            "feedback_actor_kind": actor_kind,
            "feedback_actor_id": actor_id,
            "feedback_payload": feedback_payload,
        }
    )

    if output == "json":
        typer.echo(json.dumps(result, ensure_ascii=False))
        return
    typer.echo(f"{result['feedback_id']} {result['feedback_type']} {result['session_id']}")
