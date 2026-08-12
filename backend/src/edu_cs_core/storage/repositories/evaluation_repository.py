from __future__ import annotations

import json

from edu_cs_core.storage.models import AttributionRecordModel, EvaluationRecordModel


class EvaluationRepository:
    def __init__(self, session) -> None:
        self.session = session

    def replace_evaluations(self, session_id: str, evaluations: list[dict]) -> list[EvaluationRecordModel]:
        existing = (
            self.session.query(EvaluationRecordModel)
            .filter(EvaluationRecordModel.session_id == session_id)
            .all()
        )
        for record in existing:
            self.session.query(AttributionRecordModel).filter(
                AttributionRecordModel.evaluation_id == record.evaluation_id
            ).delete()
        self.session.query(EvaluationRecordModel).filter(EvaluationRecordModel.session_id == session_id).delete()

        models: list[EvaluationRecordModel] = []
        for evaluation in evaluations:
            model = EvaluationRecordModel(
                evaluation_id=evaluation["evaluation_id"],
                session_id=session_id,
                event_id=evaluation.get("event_id"),
                evaluation_kind=evaluation["evaluation_kind"],
                label=evaluation["label"],
                signal_key=evaluation.get("signal_key"),
                value_json=json.dumps(evaluation["value"], ensure_ascii=False),
                signal_config_version=evaluation.get("signal_config_version"),
                consumption_tier_snapshot=evaluation.get("consumption_tier_snapshot"),
                lifecycle_state_snapshot=evaluation.get("lifecycle_state_snapshot"),
                confidence=str(evaluation.get("confidence")) if evaluation.get("confidence") is not None else None,
                rule_or_model_revision=evaluation.get("rule_or_model_revision"),
            )
            self.session.add(model)
            self.session.flush()

            primary = evaluation["primary_source"]
            self.session.add(
                AttributionRecordModel(
                    attribution_id=f"{model.evaluation_id}:primary",
                    evaluation_id=model.evaluation_id,
                    source_role="primary",
                    contribution_kind=primary.get("contribution_kind") or "trigger",
                    source_type=primary["source_type"],
                    source_ref=primary["source_ref"],
                    source_version=primary.get("source_version"),
                )
            )
            for index, contributing in enumerate(evaluation.get("contributing_sources", []), start=1):
                self.session.add(
                    AttributionRecordModel(
                        attribution_id=f"{model.evaluation_id}:contrib:{index}",
                        evaluation_id=model.evaluation_id,
                        source_role="contributing",
                        contribution_kind=contributing.get("contribution_kind") or "support",
                        source_type=contributing["source_type"],
                        source_ref=contributing["source_ref"],
                        source_version=contributing.get("source_version"),
                    )
                )
            models.append(model)
        return models

    def list_evaluations(self, session_id: str) -> list[EvaluationRecordModel]:
        return (
            self.session.query(EvaluationRecordModel)
            .filter(EvaluationRecordModel.session_id == session_id)
            .order_by(EvaluationRecordModel.produced_at.asc())
            .all()
        )

    def list_attributions(self, evaluation_ids: list[str]) -> list[AttributionRecordModel]:
        if not evaluation_ids:
            return []
        return (
            self.session.query(AttributionRecordModel)
            .filter(AttributionRecordModel.evaluation_id.in_(evaluation_ids))
            .all()
        )
