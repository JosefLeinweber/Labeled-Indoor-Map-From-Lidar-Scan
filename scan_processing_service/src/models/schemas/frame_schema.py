import datetime
import loguru
import pydantic
from src.utility.pydantic_schema.base_schema import BaseModel
from pydantic import Field


class FrameBase(BaseModel):
    id: int
    frame_index: int


class FrameInCreate(FrameBase):
    scan_id: int
    projection_matrix: list
    camera_pose_ar_frame: list


class FrameOutDelete(FrameBase):
    id: int
    is_deleted: bool


class FrameOut(FrameBase):
    scan_id: int
    projection_matrix: list
    camera_pose_ar_frame: list
