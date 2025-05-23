import datetime
import loguru
import pydantic
from src.utility.pydantic_schema.base_schema import BaseModel
from src.models.schemas.frame_schema import FrameOut
from pydantic import Field


class ScanBase(BaseModel):
    name: str


class ScanInCreate(ScanBase):
    user_id: int
    num_images: int


class ScanOutDelete(ScanBase):
    id: int
    is_deleted: bool


class ScanOut(ScanBase):
    id: int
    user_id: int
    num_images: int


class ScanOutWithFrames(ScanOut):
    frames: list[FrameOut]
