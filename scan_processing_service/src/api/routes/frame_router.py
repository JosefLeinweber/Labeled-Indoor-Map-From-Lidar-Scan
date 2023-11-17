import fastapi
import loguru
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)

from src.crud import frame_crud
from src.crud import scan_crud
from src.models.schemas.frame_schema import FrameInCreate, FrameOutDelete, FrameOut
from src.utility.database.db_session import get_async_session


router = fastapi.APIRouter(prefix="/frame", tags=["frame"])


@router.post(
    path="",
    name="frame:upload_frame",
    status_code=201,
    response_model=FrameOut,
)
async def upload_frame(
    new_frame: FrameInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> FrameOut:
    parent_scan = await scan_crud.get_by_id(
        db_session=db_session(), id=new_frame.scan_id
    )

    created_frame = await frame_crud.create(
        db_session=db_session(), frame=new_frame, parent_scan=parent_scan
    )

    #! The automatic conversion of snake_case to camelCase is not working for some reason => doing it manually
    return FrameOut(
        frameIndex=created_frame.frame_index,
        id=created_frame.id,
        scanId=created_frame.scan_id,
        projectionMatrix=created_frame.projection_matrix,
        cameraPoseArFrame=created_frame.camera_pose_ar_frame,
    )


@router.get(
    path="",
    name="frame:get_all_frames",
    response_model=list[FrameOut],
    status_code=200,
)
async def get_all_frames(
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> list[FrameOut]:
    try:
        all_frames = await frame_crud.get_all(db_session())
    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to get all frames with CRUD: {e}"
        )
    return [
        FrameOut(
            frameIndex=frame.frame_index,
            id=frame.id,
            scanId=frame.scan_id,
            projectionMatrix=frame.projection_matrix,
            cameraPoseArFrame=frame.camera_pose_ar_frame,
        )
        for frame in all_frames
    ]
