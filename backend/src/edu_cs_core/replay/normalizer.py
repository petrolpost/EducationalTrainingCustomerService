from __future__ import annotations

from edu_cs_core.protocol.schemas import ReplayEventInput, ReplayRequest


def normalize_replay_request(payload: dict) -> ReplayRequest:
    request = ReplayRequest.model_validate(payload)
    request.events = sorted(request.events, key=lambda event: event.seq)
    return request


def summarize_route(events: list[ReplayEventInput]) -> dict[str, str | float]:
    joined = " ".join(filter(None, (event.content for event in events)))
    if "请假" in joined:
        label = "in_service.leave_consultation"
    else:
        label = "in_service.general_support"
    return {"label": label, "confidence": 0.87}
