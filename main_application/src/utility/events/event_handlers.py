import fastapi
import typing
import loguru

from src.config.loging import setup_logging
from src.utility.events.db_events import (
    initialize_db_connection,
    terminate_db_connection,
)


def execute_backend_server_event_handler(app: fastapi.FastAPI) -> typing.Any:
    setup_logging()
    loguru.logger.info("Mounting execute backend server events...")

    async def dumy_start() -> None:
        loguru.logger.info("Starting backend server events...")

        await initialize_db_connection(app=app)

    return dumy_start


def terminate_backend_server_event_handler(app: fastapi.FastAPI) -> typing.Any:
    loguru.logger.info("Mounting terminate backend server events...")

    async def dumy_stop() -> None:
        loguru.logger.info("Terminating backend server events...")
        await terminate_db_connection(app=app)

    return dumy_stop
