from src.config.settings.base import Settings


class DevelopmentSettings(Settings):
    DESCRIPTION: str = "Development Settings | Modified FastAPI Template"
    ENVIRONMENT: str = "dev"
    DEBUG: bool = True
