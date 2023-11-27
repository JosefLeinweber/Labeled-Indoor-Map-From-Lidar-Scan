import fastapi
import loguru

# import open3d as o3d
import sqlalchemy
from sqlalchemy import exc as sqlalchemy_error
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.crud import floorplan_crud, frame_crud
from src.models.db_tables.intersection_point_table import IntersectionPoint
from src.models.schemas.frame_schema import FrameInIntersectionCalculator
from src.models.schemas.intersection_point_schema import IntersectionPointInCreate, IntersectionPointOut
from src.utility.cloud_storage.gcs_class import gcstorage
from src.utility.scan_processing.intersection_point_calculator import IntersectionPointCalculator


async def create(new_intersections: IntersectionPointInCreate, db_session) -> list[IntersectionPoint]:
    loguru.logger.info("* creating new intersection points")

    floorplan = await floorplan_crud.get_by_scan_id(new_intersections.scan_id, db_session)

    if floorplan is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Floorplan with scan id {new_intersections.scan_id} not found",
        )

    frames = await frame_crud.get_frames_by_scan_id(new_intersections.scan_id, db_session)

    if frames is None:
        raise fastapi.HTTPException(
            status_code=404,
            detail=f"Frames with scan id {new_intersections.scan_id} not found",
        )

    loguru.logger.debug(f"frames and floor plan loaded")
    loguru.logger.debug(f"len of frames: {len(frames)}")

    intersection_point_calculator = IntersectionPointCalculator(
        sorted_edged_points=floorplan.polygon_points,
        frames=[
            FrameInIntersectionCalculator(
                frameIndex=frame.frame_index,
                cameraPoseArFrame=frame.camera_pose_ar_frame,
            )
            for frame in frames
        ],
    )

    loguru.logger.debug(f"intersection point calculator created")
    loguru.logger.debug(f"len of polygon points: {len(floorplan.polygon_points)}")

    intersection_point_calculator.compute_intersections()

    loguru.logger.debug(f"len of intersections: {len(intersection_point_calculator.intersections)}")

    intersections = [
        IntersectionPoint(**intersection.model_dump()) for intersection in intersection_point_calculator.intersections
    ]
    loguru.logger.debug(f"intersections created")
    loguru.logger.debug(f"len of intersections: {len(intersections)}")

    for intersection in intersections:
        intersection.floorplan = floorplan
        db_session.add(instance=intersection)
        await db_session.commit()

    await db_session.close()

    return intersections
