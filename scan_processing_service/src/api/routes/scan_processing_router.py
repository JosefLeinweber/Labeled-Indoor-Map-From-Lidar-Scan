import fastapi
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)

from src.crud import scan_crud
from src.models.schemas.scan_schema import ScanInCreate, ScanOutDelete, ScanOut
from src.utility.database.db_session import get_async_session


router = fastapi.APIRouter(prefix="/scan_processing", tags=["Scan Processing"])


@router.post(
    path="",
    name="scan_processing:create_scan",
    status_code=201,
)
async def create_scan(
    new_scan: ScanInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> ScanOut:
    created_scan = await scan_crud.create(new_scan, db_session())
    return ScanOut(**created_scan.__dict__)


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
