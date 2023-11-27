import loguru

# import open3d as o3d
import sqlalchemy
from sqlalchemy import exc as sqlalchemy_error
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.crud import scan_crud
from src.models.db_tables.floorplan_table import Floorplan
from src.models.schemas.floorplan_schema import FloorplanInCreate, FloorplanOut
from src.utility.cloud_storage.gcs_class import gcstorage
from src.utility.scan_processing.floorplan_generator import FloorplanGenerator


async def create(new_floorplan: FloorplanInCreate, db_session) -> Floorplan:
    loguru.logger.info("* creating new floorplan")

    scan = await scan_crud.get_by_id(new_floorplan.scan_id, db_session)

    path_to_point_cloud = gcstorage.download_blob(
        bucket_name="gcs_api_demo_12353",
        blob_name="points.ply",
        project_id="scan-processing",
    )

    floorplan_generator = FloorplanGenerator(o3d.io.read_point_cloud(str(path_to_point_cloud)))

    new_floorplan = Floorplan(**new_floorplan.__dict__)
    new_floorplan.polygon_points = floorplan_generator.sorted_edge_points
    new_floorplan.scan = scan
    db_session.add(instance=new_floorplan)
    await db_session.commit()
    await db_session.refresh(instance=new_floorplan)
    await db_session.close()
    return new_floorplan


async def get_by_scan_id(scan_id: int, db_session) -> Floorplan:
    loguru.logger.info("* getting floorplan by scan id")
    try:
        select_stmt = (
            sqlalchemy.select(Floorplan).options(sqlalchemy_selectinload("*")).where(Floorplan.scan_id == scan_id)
        )
        query = await db_session.execute(statement=select_stmt)

    except sqlalchemy_error.NoResultFound as e:
        raise sqlalchemy_error.NoResultFound(f"Floorplan with scan id {scan_id} not found\n{e}")

    await db_session.close()
    return query.scalars().first()
