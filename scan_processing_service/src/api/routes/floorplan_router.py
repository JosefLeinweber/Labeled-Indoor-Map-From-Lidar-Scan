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

from src.crud import floorplan_crud
from src.models.schemas.floorplan_schema import FloorplanInCreate, FloorplanOut
from src.models.schemas.scan_schema import ScanInCreate, ScanOut, ScanOutDelete, ScanOutWithFrames
from src.utility.cloud_storage.gcs_class import get_gcstorage
from src.utility.database.db_session import get_async_session

router = fastapi.APIRouter(prefix="/floorplan", tags=["Floorplan"])


@router.post(
    path="",
    name="floorplan:generate_floor_plan_from_scan",
    response_model=FloorplanOut,
    status_code=201,
)
async def generate_floor_plan_from_scan(
    new_floorplan: FloorplanInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(get_async_session),
) -> FloorplanOut:
    try:
        created_floorplan = await floorplan_crud.create(new_floorplan, db_session())

    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Failed to generate floorplan\n{e}")
    loguru.logger.debug(f"Created floorplan: {created_floorplan.__dict__}")

    return FloorplanOut(
        name=created_floorplan.name,
        id=created_floorplan.id,
        scanId=created_floorplan.scan_id,
        polygonPoints=created_floorplan.polygon_points,
    )


@router.get(
    path="/{scan_id}",
    name="floorplan:get_floor_plan_by_scan_id",
    response_model=FloorplanOut,
    status_code=200,
)
async def get_floor_plan_by_scan_id(
    scan_id: int,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(get_async_session),
) -> FloorplanOut:
    try:
        floorplan = await floorplan_crud.get_by_scan_id(scan_id, db_session())
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f"Failed to get floorplan\n{e}")
    if floorplan is None:
        raise fastapi.HTTPException(status_code=404, detail=f"Floorplan with scan id {scan_id} not found")

    return FloorplanOut(
        name=floorplan.name,
        id=floorplan.id,
        scanId=floorplan.scan_id,
        polygonPoints=floorplan.polygon_points,
    )
