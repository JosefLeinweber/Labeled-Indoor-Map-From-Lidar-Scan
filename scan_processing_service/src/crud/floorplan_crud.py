from src.models.db_tables.floorplan_table import Floorplan
from src.models.schemas.floorplan_schema import FloorplanOut, FloorplanInCreate
import loguru
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import exc as sqlalchemy_error
from src.crud import scan_crud
from src.crud import frame_crud
from src.utility.cloud_storage.gcs_class import gcstorage
from src.utility.floorplan_generator.floorplan_generator import FloorplanGenerator
import open3d as o3d


async def create(new_floorplan: FloorplanInCreate, db_session) -> Floorplan:
    loguru.logger.info("* creating new floorplan")

    # 1. Load the scan_info from the database with scan_id

    # scan_info = await scan_crud.get_by_id(
    #     id=new_floorplan.scan_id, db_session=db_session
    # )

    # # 2. Load the frames from the database with scan_id

    # frames = await frame_crud.get_frames_by_scan_id(
    #     scan_id=new_floorplan.scan_id, db_session=db_session
    # )

    # 3. download the point cloud from gcs

    path_to_point_cloud = gcstorage.download_blob(
        bucket_name="gcs_api_demo_12353",
        blob_name="points.ply",
        project_id="scan-processing",
    )

    floorplan_generator = FloorplanGenerator(
        o3d.io.read_point_cloud(str(path_to_point_cloud))
    )

    new_floorplan = Floorplan(**new_floorplan.__dict__)
    new_floorplan.polygon = floorplan_generator.polygon
    db_session.add(instance=new_floorplan)
    await db_session.commit()
    await db_session.refresh(instance=new_floorplan)
    await db_session.close()
    return new_floorplan


async def _download_point_cloud_from_gcs(bucket_name, blob_name):
    loguru.logger.info("* Downloading point cloud from gcs")
    gcstorage.download_blob(bucket_name=bucket_name, blob_name=blob_name)
