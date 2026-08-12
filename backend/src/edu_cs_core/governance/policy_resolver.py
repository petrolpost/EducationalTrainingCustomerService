from __future__ import annotations

from edu_cs_core.governance.schemas import SignalPolicySnapshot
from edu_cs_core.storage.database import SessionLocal
from edu_cs_core.storage.repositories.signal_repository import SignalRepository


class SignalPolicyResolver:
    def __init__(self, session_factory=SessionLocal) -> None:
        self._session_factory = session_factory

    def resolve(self, signal_key: str, display_name: str) -> SignalPolicySnapshot:
        with self._session_factory() as session:
            repository = SignalRepository(session)
            profile = repository.ensure_profile(signal_key, display_name)
            session.commit()
            return SignalPolicySnapshot(
                signal_key=profile.signal_key,
                signal_config_version=profile.current_config_version,
                consumption_tier_snapshot=profile.default_consumption_tier,
                lifecycle_state_snapshot=profile.lifecycle_state,
            )
