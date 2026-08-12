from __future__ import annotations

from edu_cs_core.protocol.schemas import ReplayResult, ReplayTimeline


def serialize_replay_result(result: ReplayResult) -> dict:
    return result.model_dump()


def serialize_replay_timeline(result: ReplayTimeline) -> dict:
    return result.model_dump()
