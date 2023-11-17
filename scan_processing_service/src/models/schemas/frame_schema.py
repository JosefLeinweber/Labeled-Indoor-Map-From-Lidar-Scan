import datetime

import loguru
import pydantic
from pydantic import Field

from src.utility.pydantic_schema.base_schema import BaseModel


class FrameBase(BaseModel):
    frame_index: int


class FrameInCreate(FrameBase):
    scan_id: int
    projection_matrix: list
    camera_pose_ar_frame: list


class FrameOutDelete(FrameBase):
    id: int
    is_deleted: bool


class FrameOut(FrameBase):
    id: int
    scan_id: int
    projection_matrix: list
    camera_pose_ar_frame: list


class FrameInIntersectionCalculator(FrameBase):
    camera_pose_ar_frame: list
