"""
get async sesison through function
"""

from typing import Generator

from src.utility.database.db_class import db


async def get_async_session() -> Generator:  # type: ignore
    try:
        yield db.async_session
    except Exception as e:
        print(e)
        await db.async_session().rollback()
    finally:
        await db.async_session().close()
