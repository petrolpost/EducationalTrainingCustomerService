from __future__ import annotations

from datetime import datetime, timezone

from edu_cs_core.storage.models import SignalLifecycleEventModel, SignalProfileModel


class SignalRepository:
    def __init__(self, session) -> None:
        self.session = session

    def ensure_profile(
        self,
        signal_key: str,
        display_name: str,
        *,
        consumption_tier: str = "observe",
        lifecycle_state: str = "experimental",
        config_version: str = "0.1.0",
    ) -> SignalProfileModel:
        profile = self.session.get(SignalProfileModel, signal_key)
        if profile is None:
            profile = SignalProfileModel(
                signal_key=signal_key,
                display_name=display_name,
                default_consumption_tier=consumption_tier,
                lifecycle_state=lifecycle_state,
                current_config_version=config_version,
            )
            self.session.add(profile)
        return profile

    def get_profile(self, signal_key: str) -> SignalProfileModel | None:
        return self.session.get(SignalProfileModel, signal_key)

    def create_lifecycle_event(self, **kwargs) -> SignalLifecycleEventModel:
        event = SignalLifecycleEventModel(
            lifecycle_event_id=f"{kwargs['signal_key']}:{int(datetime.now(timezone.utc).timestamp())}",
            **kwargs,
        )
        self.session.add(event)
        return event
