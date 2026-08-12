from __future__ import annotations

import json

from edu_cs_core.protocol.schemas import ReplayEventInput, ReplaySessionInput
from edu_cs_core.storage.models import ConversationEventModel, ReplaySessionModel


class ReplayRepository:
    def __init__(self, session) -> None:
        self.session = session

    def upsert_session(self, replay_session: ReplaySessionInput, event_count: int) -> ReplaySessionModel:
        model = self.session.get(ReplaySessionModel, replay_session.session_id)
        if model is None:
            model = ReplaySessionModel(
                session_id=replay_session.session_id,
                tenant_id=replay_session.tenant_id,
                school_id=replay_session.school_id,
                source_kind=replay_session.source_kind,
                event_count=event_count,
                status="running",
            )
            self.session.add(model)
        else:
            model.event_count = event_count
            model.status = "running"
        return model

    def replace_events(self, session_id: str, events: list[ReplayEventInput]) -> list[ConversationEventModel]:
        self.session.query(ConversationEventModel).filter(ConversationEventModel.session_id == session_id).delete()
        models: list[ConversationEventModel] = []
        for event in events:
            model = ConversationEventModel(
                event_id=event.event_id,
                session_id=session_id,
                seq=event.seq,
                occurred_at=event.occurred_at,
                event_type=event.event_type,
                actor_kind=event.actor_kind,
                actor_id=event.actor_id,
                content=event.content,
                channel=event.channel,
                metadata_json=json.dumps(event.metadata, ensure_ascii=False),
                extension_json=json.dumps(event.extensions, ensure_ascii=False),
            )
            self.session.add(model)
            models.append(model)
        return models

    def get_session(self, session_id: str) -> ReplaySessionModel | None:
        return self.session.get(ReplaySessionModel, session_id)

    def list_events(self, session_id: str) -> list[ConversationEventModel]:
        return (
            self.session.query(ConversationEventModel)
            .filter(ConversationEventModel.session_id == session_id)
            .order_by(ConversationEventModel.seq.asc())
            .all()
        )
