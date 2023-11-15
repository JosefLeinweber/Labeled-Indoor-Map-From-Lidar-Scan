import fastapi
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)
from src.utility.database.db_session import get_async_session


router = fastapi.APIRouter(prefix="/scan_processing", tags=["Scan Processing"])


@router.get(
    path="",
    name="scan_processing:main",
    status_code=201,
)
async def processing_scan(
    scan_id: int,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> dict:
    return {"message": "Scan Processing"}
