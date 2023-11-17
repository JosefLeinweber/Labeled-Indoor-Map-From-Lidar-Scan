import datetime

import pydantic
import sqlalchemy
from sqlalchemy.orm import (
    Mapped as SQLAlchemyMapped,
    mapped_column as sqlalchemy_mapped_column,
    relationship as sqlalchemy_relationship,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.utility.database.base_table import DBBaseTable


class IntersectionPoint(DBBaseTable):
    __tablename__ = "intersection_point"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    frame_index: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
    coordinates: SQLAlchemyMapped[list] = sqlalchemy_mapped_column(sqlalchemy.JSON, nullable=False)
    classification: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=True)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        server_default=sqlalchemy_functions.now(),
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    floorplan_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        sqlalchemy.ForeignKey("floorplan.id"), nullable=False
    )
    floorplan = sqlalchemy_relationship("Floorplan", back_populates="intersection_point")

    __mapper_args__ = {"eager_defaults": True}
