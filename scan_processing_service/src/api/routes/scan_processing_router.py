import fastapi
import loguru
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
    try:
        created_scan = await scan_crud.create(new_scan, db_session())

    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to create scan with CRUD: {e}"
        )
    loguru.logger.debug(f"Created scan: {created_scan.__dict__}")

    #! The automatic conversion of snake_case to camelCase is not working for some reason => doing it manually
    return ScanOut(
        name=created_scan.name,
        id=created_scan.id,
        userId=created_scan.user_id,
        numImages=created_scan.num_images,
    )


# @router.get(
#     path="/{id}",
#     name="scan_processing:get_scan_by_id",
#     response_model=ScanOut,
#     status_code=200,
# )
