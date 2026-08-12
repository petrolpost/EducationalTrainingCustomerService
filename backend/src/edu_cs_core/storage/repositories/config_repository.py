from __future__ import annotations

import json

from edu_cs_core.storage.models import BaselineConfigModel


class ConfigRepository:
    def __init__(self, session) -> None:
        self.session = session

    def save(self, config_version: str, spec_version: str, payload: dict, status: str = "draft") -> BaselineConfigModel:
        model = BaselineConfigModel(
            config_version=config_version,
            spec_version=spec_version,
            schema_version="1.0",
            config_payload=json.dumps(payload, ensure_ascii=False),
            status=status,
        )
        self.session.merge(model)
        return model

    def get(self, config_version: str) -> BaselineConfigModel | None:
        return self.session.get(BaselineConfigModel, config_version)
