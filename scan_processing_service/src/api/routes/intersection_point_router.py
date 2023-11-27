import pathlib

import fastapi
import loguru

# import numpy as np
# import open3d as o3d
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)

from src.crud import floorplan_crud, intersection_point_crud, scan_crud
from src.models.schemas.intersection_point_schema import IntersectionPointInCreate, IntersectionPointOut
from src.models.schemas.scan_schema import ScanInCreate, ScanOut, ScanOutDelete, ScanOutWithFrames
from src.utility.cloud_storage.gcs_class import get_gcstorage
from src.utility.database.db_session import get_async_session

router = fastapi.APIRouter(prefix="/intersection_point", tags=["Intersection Point"])


@router.post(
    path="",
    name="intersection_point:compute_intersections",
    response_model=list[IntersectionPointOut],
    status_code=201,
)
async def compute_intersections(
    new_intersections: IntersectionPointInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(get_async_session),
) -> list[IntersectionPointOut]:
    try:
        created_intersections = await intersection_point_crud.create(new_intersections, db_session())

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Failed to compute intersections\n{e}")

    return [
        IntersectionPointOut(
            id=intersection.id,
            frameIndex=intersection.frame_index,
            coordinates=intersection.coordinates,
            classification="empty",
        )
        for intersection in created_intersections
    ]
