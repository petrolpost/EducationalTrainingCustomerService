from __future__ import annotations

import json
from pathlib import Path

from .schema import BaselineConfigModel


DEFAULT_CONFIG_PATH = Path("backend/config/baseline.json")


def load_baseline_config(path: Path | None = None) -> BaselineConfigModel:
    config_path = path or DEFAULT_CONFIG_PATH
    if not config_path.exists():
        return BaselineConfigModel(config_version="0.1.0", spec_version="001-edu-cs-core")
    return BaselineConfigModel.model_validate(json.loads(config_path.read_text(encoding="utf-8")))
