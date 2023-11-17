import datetime

import loguru
import pydantic
from pydantic import Field

from src.utility.pydantic_schema.base_schema import BaseModel


class FloorplanBase(BaseModel):
    name: str


class FloorplanInCreate(FloorplanBase):
    scan_id: int


class FloorplanOutDelete(FloorplanBase):
    id: int
    is_deleted: bool


class FloorplanOut(FloorplanBase):
    id: int
    scan_id: int
    polygon_points: list
