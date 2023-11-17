import fastapi
import loguru
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)

from src.crud import scan_crud
from src.crud import frame_crud
from src.models.schemas.scan_schema import (
    ScanInCreate,
    ScanOutDelete,
    ScanOut,
    ScanOutWithFrames,
)
from src.models.schemas.frame_schema import FrameOut
from src.utility.database.db_session import get_async_session


router = fastapi.APIRouter(prefix="/scan", tags=["Scan"])


@router.post(
    path="",
    name="scan::upload_scan",
    status_code=201,
)
async def upload_scan(
    new_scan: ScanInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> ScanOut:
    try:
        created_scan = await scan_crud.create(new_scan, db_session())

    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to upload scan\n{e}"
        )
    loguru.logger.debug(f"Created scan: {created_scan.__dict__}")

    #! The automatic conversion of snake_case to camelCase is not working for some reason => doing it manually
    return ScanOut(
        name=created_scan.name,
        id=created_scan.id,
        userId=created_scan.user_id,
        numImages=created_scan.num_images,
    )


@router.get(
    path="/{id}",
    name="scan:get_scan_by_id",
    response_model=ScanOutWithFrames,
    status_code=200,
)
async def get_scan_by_id(
    id: int,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> ScanOutWithFrames:
    try:
        scan = await scan_crud.get_by_id(id=id, db_session=db_session())
        frames = await frame_crud.get_frames_by_scan_id(
            scan_id=id, db_session=db_session()
        )
    except Exception as e:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Scan with id: {id} does not exist\n{e}"
        )
    loguru.logger.debug(f"Found scan: {scan.__dict__}")

    #! The automatic conversion of snake_case to camelCase is not working for some reason => doing it manually
    return ScanOutWithFrames(
        name=scan.name,
        id=scan.id,
        userId=scan.user_id,
        numImages=scan.num_images,
        frames=[
            FrameOut(
                frameIndex=frame.frame_index,
                id=frame.id,
                scanId=frame.scan_id,
                projectionMatrix=frame.projection_matrix,
                cameraPoseArFrame=frame.camera_pose_ar_frame,
            )
            for frame in frames
        ],
    )
