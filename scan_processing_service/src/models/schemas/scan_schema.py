import datetime
import loguru
import pydantic
from src.utility.pydantic_schema.base_schema import BaseModel


class ScanBase(BaseModel):
    scan_name: str
    scan_id: int


class ScanInCreate(ScanBase):
    user_id: int
    num_images: int
    last_camera_pose: dict


class ScanInDelete(ScanBase):
    is_deleted: bool
