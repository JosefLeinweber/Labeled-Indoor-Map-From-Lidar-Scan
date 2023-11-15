from src.config.settings.base import Settings


class ProductionSettings(Settings):
    DESCRIPTION: str = "Production Settings | Modified FastAPI Template"
    ENVIRONMENT: str = "prod"
    DEBUG: bool = False
    TESTING: bool = False
