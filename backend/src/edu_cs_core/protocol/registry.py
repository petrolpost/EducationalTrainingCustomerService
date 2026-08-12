from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


class ProtocolRegistry:
    """Minimal schema-version registry for replay readers."""

    def __init__(self) -> None:
        self._readers: dict[str, Callable[[dict], T]] = {}

    def register(self, schema_version: str, reader: Callable[[dict], T]) -> None:
        self._readers[schema_version] = reader

    def read(self, schema_version: str, payload: dict) -> T:
        if schema_version not in self._readers:
            raise KeyError(f"Unsupported schema version: {schema_version}")
        return self._readers[schema_version](payload)


registry = ProtocolRegistry()
