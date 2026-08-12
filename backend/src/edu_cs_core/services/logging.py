from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any


def _json_default(value: Any) -> Any:
    if isinstance(value, set):
        return sorted(value)
    return str(value)


class StructuredLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        fields = getattr(record, "fields", None)
        if isinstance(fields, dict):
            payload.update(fields)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=_json_default)


def configure_logging(level: int | str = logging.INFO) -> None:
    logger = logging.getLogger("edu_cs_core")
    if getattr(logger, "_edu_cs_configured", False):
        logger.setLevel(level)
        return

    handler = logging.StreamHandler()
    handler.setFormatter(StructuredLogFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    logger._edu_cs_configured = True  # type: ignore[attr-defined]


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    if name.startswith("edu_cs_core"):
        return logging.getLogger(name)
    return logging.getLogger(f"edu_cs_core.{name}")


def log_event(logger: logging.Logger, event: str, *, level: int = logging.INFO, **fields: Any) -> None:
    logger.log(level, event, extra={"fields": fields})
