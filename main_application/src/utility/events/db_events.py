import typing
import fastapi
import loguru

from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.dialects.postgresql.asyncpg import (
    AsyncAdapt_asyncpg_connection as AsyncPGConnection,
)
from sqlalchemy.pool.base import _ConnectionRecord as ConnectionRecord
from sqlalchemy import event


from src.utility.database.db_class import db
from src.models.db_tables.table_collection import DBBaseTable


async def initialize_db_connection(app: fastapi.FastAPI) -> None:
    loguru.logger.info("Initializing database connection...")

    app.state.db = db

    async with app.state.db.async_engine.begin() as conn:
        await initialize_db_tables(conn=conn)

    loguru.logger.info("Database connection initialized!")


async def terminate_db_connection(app: fastapi.FastAPI) -> None:
    loguru.logger.info("Terminating database connection...")

    app.state.db.async_engine.dispose()

    loguru.logger.info("Database connection terminated!")


async def initialize_db_tables(conn: AsyncConnection) -> None:
    loguru.logger.info("Initializing database tables...")

    await conn.run_sync(DBBaseTable.metadata.drop_all)  # type: ignore

    await conn.run_sync(DBBaseTable.metadata.create_all)

    loguru.logger.info("Database tables initialized!")


@event.listens_for(target=db.async_engine.sync_engine, identifier="connect")
def inspect_db_server_on_connection(
    db_api_connection: AsyncPGConnection, connection_record: ConnectionRecord
) -> None:
    loguru.logger.info(f"New DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Connection Record ---\n {connection_record}")


@event.listens_for(target=db.async_engine.sync_engine, identifier="close")
def inspect_db_server_on_close(
    db_api_connection: AsyncPGConnection, connection_record: ConnectionRecord
) -> None:
    loguru.logger.info(f"Closing DB API Connection ---\n {db_api_connection}")
    loguru.logger.info(f"Closed Connection Record ---\n {connection_record}")
