from __future__ import annotations

import json
import logging

from edu_cs_core.protocol.schemas import EvaluationOutput, ReplayResult, ReplayTimeline, SourceSummary
from edu_cs_core.services.signal_snapshot_service import SignalSnapshotService
from edu_cs_core.services.logging import get_logger, log_event
from edu_cs_core.replay.normalizer import normalize_replay_request, summarize_route
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.evaluation_repository import EvaluationRepository
from edu_cs_core.storage.repositories.replay_repository import ReplayRepository


logger = get_logger(__name__)


class ReplayProcessor:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory
        self._signal_snapshot_service = SignalSnapshotService()

    def process(self, payload: dict) -> ReplayResult:
        request = normalize_replay_request(payload)
        log_event(
            logger,
            "replay.process.started",
            session_id=request.session.session_id,
            tenant_id=request.session.tenant_id,
            school_id=request.session.school_id,
            event_count=len(request.events),
            schema_version=request.schema_version,
        )
        route = summarize_route(request.events)
        evaluations = self._build_evaluations(request, route, self._signal_snapshot_service)

        with self._session_factory() as session:
            replay_repo = ReplayRepository(session)
            evaluation_repo = EvaluationRepository(session)

            replay_session = replay_repo.upsert_session(request.session, len(request.events))
            replay_repo.replace_events(replay_session.session_id, request.events)
            evaluation_repo.replace_evaluations(replay_session.session_id, evaluations)
            replay_session.status = "completed"
            session.commit()

        log_event(
            logger,
            "replay.process.completed",
            session_id=request.session.session_id,
            tenant_id=request.session.tenant_id,
            school_id=request.session.school_id,
            status="completed",
            route_label=route["label"],
            evaluation_count=len(evaluations),
        )
        return ReplayResult(
            session_id=request.session.session_id,
            status="completed",
            route=route,
            evaluations=[EvaluationOutput.model_validate(evaluation) for evaluation in evaluations],
        )

    def get_summary(self, session_id: str) -> dict:
        with self._session_factory() as session:
            replay_repo = ReplayRepository(session)
            evaluation_repo = EvaluationRepository(session)
            replay_session = replay_repo.get_session(session_id)
            if replay_session is None:
                log_event(logger, "replay.summary.not_found", level=logging.WARNING, session_id=session_id)
                raise KeyError(session_id)
            evaluations = evaluation_repo.list_evaluations(session_id)
            summary = {
                "session_id": replay_session.session_id,
                "status": replay_session.status,
                "tenant_id": replay_session.tenant_id,
                "school_id": replay_session.school_id,
                "event_count": replay_session.event_count,
                "evaluation_count": len(evaluations),
            }
            log_event(
                logger,
                "replay.summary.loaded",
                session_id=session_id,
                tenant_id=replay_session.tenant_id,
                school_id=replay_session.school_id,
                evaluation_count=len(evaluations),
            )
            return summary

    def get_timeline(self, session_id: str) -> ReplayTimeline:
        with self._session_factory() as session:
            replay_repo = ReplayRepository(session)
            evaluation_repo = EvaluationRepository(session)
            replay_session = replay_repo.get_session(session_id)
            if replay_session is None:
                log_event(logger, "replay.timeline.not_found", level=logging.WARNING, session_id=session_id)
                raise KeyError(session_id)
            events = replay_repo.list_events(session_id)
            evaluations = evaluation_repo.list_evaluations(session_id)
            attributions = evaluation_repo.list_attributions([evaluation.evaluation_id for evaluation in evaluations])
            grouped_attributions: dict[str, list] = {}
            for attribution in attributions:
                grouped_attributions.setdefault(attribution.evaluation_id, []).append(attribution)

            timeline_evaluations = []
            for evaluation in evaluations:
                primary = None
                contributing = []
                for attribution in grouped_attributions.get(evaluation.evaluation_id, []):
                    item = {
                        "source_type": attribution.source_type,
                        "source_ref": attribution.source_ref,
                        "source_version": attribution.source_version,
                        "contribution_kind": attribution.contribution_kind,
                    }
                    if attribution.source_role == "primary":
                        primary = item
                    else:
                        contributing.append(item)
                timeline_evaluations.append(
                    {
                        "evaluation_id": evaluation.evaluation_id,
                        "evaluation_kind": evaluation.evaluation_kind,
                        "label": evaluation.label,
                        "signal_key": evaluation.signal_key,
                        "signal_config_version": evaluation.signal_config_version,
                        "consumption_tier_snapshot": evaluation.consumption_tier_snapshot,
                        "lifecycle_state_snapshot": evaluation.lifecycle_state_snapshot,
                        "value": json.loads(evaluation.value_json),
                        "primary_source": primary,
                        "contributing_sources": contributing,
                    }
                )

            timeline = ReplayTimeline(
                session_id=replay_session.session_id,
                status=replay_session.status,
                events=[
                    {
                        "event_id": event.event_id,
                        "seq": event.seq,
                        "occurred_at": event.occurred_at.isoformat(),
                        "event_type": event.event_type,
                        "actor_kind": event.actor_kind,
                        "content": event.content,
                    }
                    for event in events
                ],
                evaluations=timeline_evaluations,
            )
            log_event(
                logger,
                "replay.timeline.loaded",
                session_id=session_id,
                tenant_id=replay_session.tenant_id,
                school_id=replay_session.school_id,
                event_count=len(events),
                evaluation_count=len(evaluations),
            )
            return timeline

    @staticmethod
    def _build_evaluations(request, route: dict, signal_snapshot_service: SignalSnapshotService) -> list[dict]:
        primary_source = SourceSummary(source_type="rule", source_ref="routing-rule.v1", source_version="1.0")
        evaluations = [
            {
                "evaluation_id": f"{request.session.session_id}:route",
                "evaluation_kind": "route",
                "label": route["label"],
                "value": {"summary": "route selected from replay content"},
                "primary_source": primary_source.model_dump(),
                "contributing_sources": [],
                "confidence": route["confidence"],
                "rule_or_model_revision": "routing-rule.v1",
            }
        ]
        joined = " ".join(filter(None, (event.content for event in request.events)))
        if "请假" in joined:
            attention_snapshot = signal_snapshot_service.snapshot("attention_shift", "Attention Shift")
            evaluations.append(
                {
                    "evaluation_id": f"{request.session.session_id}:signal:attention_shift",
                    "evaluation_kind": "signal",
                    "label": "attention_shift",
                    "signal_key": attention_snapshot["signal_key"],
                    "signal_config_version": attention_snapshot["signal_config_version"],
                    "consumption_tier_snapshot": attention_snapshot["consumption_tier_snapshot"],
                    "lifecycle_state_snapshot": attention_snapshot["lifecycle_state_snapshot"],
                    "value": {"status": "observe", "summary": "Customer focus remains on leave-rule clarification"},
                    "primary_source": {
                        "source_type": "rule",
                        "source_ref": "signal-attention.v1",
                        "source_version": "0.1.0",
                    },
                    "contributing_sources": [],
                    "confidence": 0.66,
                    "rule_or_model_revision": "signal-attention.v1",
                }
            )
            evaluations.append(
                {
                    "evaluation_id": f"{request.session.session_id}:risk:leave_followup_gap",
                    "evaluation_kind": "risk",
                    "label": "leave_followup_gap",
                    "value": {
                        "severity": "medium",
                        "summary": "Detected a risk that the leave-rule question may remain unresolved without explicit staff follow-up.",
                    },
                    "primary_source": {
                        "source_type": "rule",
                        "source_ref": "risk-leave-followup.v1",
                        "source_version": "1.0",
                    },
                    "contributing_sources": [
                        {
                            "source_type": "rule",
                            "source_ref": "signal-attention.v1",
                            "source_version": "0.1.0",
                            "contribution_kind": "support",
                        }
                    ],
                    "confidence": 0.64,
                    "rule_or_model_revision": "risk-leave-followup.v1",
                }
            )
            evaluations.append(
                {
                    "evaluation_id": f"{request.session.session_id}:action:leave_policy_followup",
                    "evaluation_kind": "action_recommendation",
                    "label": "leave_policy_followup",
                    "value": {
                        "recommended_action": "clarify_leave_policy",
                        "summary": "Recommend that staff answer leave-policy rules and confirm the student's next required step.",
                    },
                    "primary_source": {
                        "source_type": "rule",
                        "source_ref": "action-leave-followup.v1",
                        "source_version": "1.0",
                    },
                    "contributing_sources": [
                        {
                            "source_type": "rule",
                            "source_ref": "routing-rule.v1",
                            "source_version": "1.0",
                            "contribution_kind": "trigger",
                        }
                    ],
                    "confidence": 0.72,
                    "rule_or_model_revision": "action-leave-followup.v1",
                }
            )
            evaluations.append(
                {
                    "evaluation_id": f"{request.session.session_id}:summary",
                    "evaluation_kind": "summary",
                    "label": "leave_request_detected",
                    "value": {"summary": "Detected leave-related support request in replay content"},
                    "primary_source": {
                        "source_type": "rule",
                        "source_ref": "summary-rule.v1",
                        "source_version": "1.0",
                    },
                    "contributing_sources": [
                        {
                            "source_type": "model",
                            "source_ref": "dialog-model",
                            "source_version": "0.1",
                            "contribution_kind": "support",
                        }
                    ],
                    "confidence": 0.75,
                    "rule_or_model_revision": "summary-rule.v1",
                }
            )
        return evaluations
