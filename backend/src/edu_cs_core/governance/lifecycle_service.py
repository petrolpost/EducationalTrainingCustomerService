from __future__ import annotations

from datetime import datetime, timezone
import logging

from edu_cs_core.governance.schemas import SignalLifecycleChange
from edu_cs_core.services.logging import get_logger, log_event
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.signal_repository import SignalRepository


logger = get_logger(__name__)


class SignalLifecycleService:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory

    def ensure_profile(self, signal_key: str, display_name: str) -> None:
        with self._session_factory() as session:
            repository = SignalRepository(session)
            repository.ensure_profile(signal_key, display_name)
            session.commit()
        log_event(logger, "signal.profile.ensured", signal_key=signal_key, display_name=display_name)

    def record_event(self, **payload) -> None:
        change = SignalLifecycleChange.model_validate(payload)
        with self._session_factory() as session:
            repository = SignalRepository(session)
            profile = repository.get_profile(change.signal_key)
            if profile is None:
                log_event(logger, "signal.lifecycle.missing_profile", level=logging.WARNING, signal_key=change.signal_key)
                raise KeyError(change.signal_key)
            if change.governance_tier == "major" and not change.validation_report_ref:
                log_event(
                    logger,
                    "signal.lifecycle.invalid_major_change",
                    level=logging.WARNING,
                    signal_key=change.signal_key,
                    signal_config_version=change.signal_config_version,
                )
                raise ValueError("major governance changes require validation_report_ref")
            if (
                change.from_lifecycle_state == change.to_lifecycle_state
                and change.from_consumption_tier == change.to_consumption_tier
            ):
                log_event(
                    logger,
                    "signal.lifecycle.noop_rejected",
                    level=logging.WARNING,
                    signal_key=change.signal_key,
                    signal_config_version=change.signal_config_version,
                )
                raise ValueError("at least one governance axis must change")

            repository.create_lifecycle_event(
                signal_key=change.signal_key,
                signal_config_version=change.signal_config_version,
                governance_tier=change.governance_tier,
                change_type=change.change_type,
                from_lifecycle_state=change.from_lifecycle_state,
                to_lifecycle_state=change.to_lifecycle_state,
                from_consumption_tier=change.from_consumption_tier,
                to_consumption_tier=change.to_consumption_tier,
                validation_report_ref=change.validation_report_ref,
                approved_by=change.approved_by,
                approved_at=datetime.now(timezone.utc),
                decision_note=None,
            )

            if change.to_lifecycle_state is not None:
                profile.lifecycle_state = change.to_lifecycle_state
            if change.to_consumption_tier is not None:
                profile.default_consumption_tier = change.to_consumption_tier
            profile.current_config_version = change.signal_config_version
            session.commit()
        log_event(
            logger,
            "signal.lifecycle.recorded",
            signal_key=change.signal_key,
            governance_tier=change.governance_tier,
            change_type=change.change_type,
            from_lifecycle_state=change.from_lifecycle_state,
            to_lifecycle_state=change.to_lifecycle_state,
            from_consumption_tier=change.from_consumption_tier,
            to_consumption_tier=change.to_consumption_tier,
            signal_config_version=change.signal_config_version,
            approved_by=change.approved_by,
        )
