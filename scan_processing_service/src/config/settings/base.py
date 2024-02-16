import pydantic
import pydantic_settings
import pathlib
import decouple


ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class Settings(pydantic_settings.BaseSettings):
    """
    --------------------Description--------------------
    * Base settings for the FastAPI application
    * All settings are loaded from the `.env` file
    * Different environments inherit from this class and can override the settings
    for their specific needs
    """

    # ---------------------General---------------------
    TITLE: str = "Modified FastAPI Template"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = decouple.config("DEBUG", cast=bool)  # type: ignore
    ENVIRONMENT: str = decouple.config("ENVIRONMENT", cast=str)  # type: ignore
    TESTING: bool = decouple.config("TESTING", cast=bool)  # type: ignore
    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)  # type: ignore
    STATIC_FILE_DIRECTORY: str = decouple.config("STATIC_FILE_DIRECTORY", cast=str)  # type: ignore

    # ---------------------CORSMiddleware---------------------
    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        decouple.config("ALLOWED_ORIGIN_FRONTEND_LOCALHOST_DEFAULT", cast=str),  # type: ignore
        decouple.config("ALLOWED_ORIGIN_FRONTEND_LOCALHOST_CUSTOM", cast=str),  # type: ignore
        decouple.config("ALLOWED_ORIGIN_FRONTEND_DOCKER", cast=str),  # type: ignore
        decouple.config("ALLOWED_ORIGIN_FRONTEND_PRODUCTION", cast=str),  # type: ignore
    ]
    ALLOWED_METHODS: list[str] = [decouple.config("ALLOWED_METHOD_1")]  # type: ignore
    ALLOWED_HEADERS: list[str] = [decouple.config("ALLOWED_HEADER_1")]  # type: ignore

    # ---------------------Postgres---------------------
    POSTGRES_USERNAME: str = decouple.config("POSTGRES_USERNAME", cast=str)  # type: ignore
    POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)  # type: ignore
    POSTGRES_DEV_DB: str = decouple.config("POSTGRES_DEV_DB", cast=str)  # type: ignore
    POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)  # type: ignore
    POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str)  # type: ignore
    POSTGRES_DEV_HOST: str = decouple.config("POSTGRES_DEV_HOST", cast=str)  # type: ignore

    # ---------------------Databases---------------------
    POSTGRES_ECHO: bool = decouple.config("POSTGRES_ECHO", cast=bool)  # type: ignore
    DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int)  # type: ignore
    DB_MAX_OVERFLOW: int = decouple.config("DB_MAX_OVERFLOW", cast=int)  # type: ignore

    # ---------------------Cloud Storage---------------------
    GCLOUD_TYPE: str = decouple.config("GCLOUD_TYPE", cast=str)  # type: ignore
    GCLOUD_PROJECT_ID: str = decouple.config("GCLOUD_PROJECT_ID", cast=str)  # type: ignore
    GCLOUD_PRIVATE_KEY_ID: str = decouple.config("GCLOUD_PRIVATE_KEY_ID", cast=str)  # type: ignore
    GCLOUD_PRIVATE_KEY: str = decouple.config("GCLOUD_PRIVATE_KEY", cast=str)  # type: ignore
    GCLOUD_CLIENT_EMAIL: str = decouple.config("GCLOUD_CLIENT_EMAIL", cast=str)  # type: ignore
    GCLOUD_CLIENT_ID: str = decouple.config("GCLOUD_CLIENT_ID", cast=str)  # type: ignore
    GCLOUD_AUTH_URI: str = decouple.config("GCLOUD_AUTH_URI", cast=str)  # type: ignore
    GCLOUD_TOKEN_URI: str = decouple.config("GCLOUD_TOKEN_URI", cast=str)  # type: ignore
    GCLOUD_AUTH_PROVIDER_CERT_URL: str = decouple.config("GCLOUD_AUTH_PROVIDER_CERT_URL", cast=str)  # type: ignore
    GCLOUD_CLIENT_CERT_URL: str = decouple.config("GCLOUD_CLIENT_CERT_URL", cast=str)  # type: ignore

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/scan_processing_service.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` instance attributes with the custom values defined in `Settings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
        }
