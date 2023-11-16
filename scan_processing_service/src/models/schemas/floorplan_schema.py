import datetime
import loguru
import pydantic
from src.utility.pydantic_schema.base_schema import BaseModel
from pydantic import Field


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
    polygon: list
