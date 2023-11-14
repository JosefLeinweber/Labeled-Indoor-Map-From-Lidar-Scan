from functools import lru_cache

import decouple

from src.config.settings.base import Settings
from src.config.settings.development import DevelopmentSettings
from src.config.settings.production import ProductionSettings


class SettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> Settings:
        if self.environment == "dev":
            return DevelopmentSettings()

        if self.environment == "prod":
            return ProductionSettings()

        else:
            raise ValueError(f"Invalid environment: {self.environment}")


@lru_cache()
def get_settings() -> Settings:
    return SettingsFactory(
        environment=decouple.config("ENVIRONMENT", default="dev", cast=str)
    )()


settings: Settings = get_settings()
