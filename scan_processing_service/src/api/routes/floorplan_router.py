import fastapi
import loguru
import pathlib

import open3d as o3d
import numpy as np

from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)

from src.crud import floorplan_crud
from src.models.schemas.scan_schema import (
    ScanInCreate,
    ScanOutDelete,
    ScanOut,
    ScanOutWithFrames,
)
from src.models.schemas.floorplan_schema import FloorplanOut, FloorplanInCreate
from src.utility.database.db_session import get_async_session
from src.utility.cloud_storage.gcs_class import get_gcstorage


router = fastapi.APIRouter(prefix="/floorplan", tags=["Floorplan"])


@router.post(
    path="",
    name="floorplan:generate_floor_plan_from_scan",
    response_model=FloorplanOut,
    status_code=200,
)
async def generate_floor_plan_from_scan(
    new_floorplan: FloorplanInCreate,
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> FloorplanOut:
    try:
        created_floorplan = await floorplan_crud.create(new_floorplan, db_session())

    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to generate floorplan\n{e}"
        )
    loguru.logger.debug(f"Created floorplan: {created_floorplan.__dict__}")

    return FloorplanOut(
        name=created_floorplan.name,
        id=created_floorplan.id,
        scanId=created_floorplan.scan_id,
        polygon=created_floorplan.polygon,
    )


@router.get(
    path="/reading_files",
    name="floorplan:testing_gcs",
    response_model=dict,
    status_code=200,
)
async def testing_gcs(
    db_session: sqlalchemy_async_sessionmaker[SQLAlchemyAsyncSession] = fastapi.Depends(
        get_async_session
    ),
) -> dict:
    try:
        loguru.logger.debug("* Testing GCS")
        working_dir = pathlib.Path.cwd()
        downloads_folder = working_dir.joinpath("downloads")
        gcs = get_gcstorage()
        loguru.logger.debug(f"List of buckets: {gcs.list_buckets()}")
        bucket_gcs = gcs.get_bucket("gcs_api_demo_12353", project_id="scan-processing")
        loguru.logger.debug(
            f"List of blobs: {[blob.name for blob in bucket_gcs.list_blobs()]}"
        )
        blob = bucket_gcs.blob("points.ply")

        path_download = downloads_folder.joinpath(blob.name)
        loguru.logger.debug(f"Download path: {path_download}")
        if not path_download.parent.exists():
            path_download.parent.mkdir(parents=True)
        blob.download_to_filename(str(path_download))

    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to list buckets\n{e}"
        )

    try:
        pcd = o3d.io.read_point_cloud(str(path_download))

    except Exception as e:
        raise fastapi.HTTPException(
            status_code=500, detail=f"Failed to create point cloud\n{e}"
        )

    return {
        "success": True if blob else False,
        "blob content type": blob.content_type,
        "pcd size": len(pcd.points),
    }
