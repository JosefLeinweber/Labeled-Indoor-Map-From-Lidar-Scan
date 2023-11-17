import datetime

import loguru
import pydantic
from pydantic import Field

from src.utility.pydantic_schema.base_schema import BaseModel


class IntersectionPointBase(BaseModel):
    id: int


class IntersectionPointInCreate(IntersectionPointBase):
    scan_id: int


class IntersectionPointInUpdate(IntersectionPointBase):
    classification: str | None


class IntersectionPointOutDelete(IntersectionPointBase):
    id: int
    is_deleted: bool


class IntersectionPointOut(IntersectionPointBase):
    id: int
    frame_index: int
    coordinates: list
    classification: str | None


class IntersectionPointOutCalculator(BaseModel):
    coordinates: list
    frame_index: int
