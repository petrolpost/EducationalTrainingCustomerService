from __future__ import annotations

from edu_cs_core.governance.policy_resolver import SignalPolicyResolver


class SignalSnapshotService:
    def __init__(self, resolver: SignalPolicyResolver | None = None) -> None:
        self._resolver = resolver or SignalPolicyResolver()

    def snapshot(self, signal_key: str, display_name: str) -> dict[str, str]:
        snapshot = self._resolver.resolve(signal_key, display_name)
        return snapshot.model_dump()
