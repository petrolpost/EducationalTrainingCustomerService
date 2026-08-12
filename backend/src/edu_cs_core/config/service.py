from __future__ import annotations

import json
from pathlib import Path

from edu_cs_core.config.schema import BaselineConfigModel


class ConfigService:
    def validate_file(self, path: Path) -> BaselineConfigModel:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return BaselineConfigModel.model_validate(payload)

    def diff_files(self, left: Path, right: Path) -> dict:
        left_model = self.validate_file(left)
        right_model = self.validate_file(right)
        return {
            "changed": left_model.model_dump() != right_model.model_dump(),
            "left_version": left_model.config_version,
            "right_version": right_model.config_version,
        }
