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


class Floorplan(DBBaseTable):
    __tablename__ = "floorplan"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=False)
    polygon_points: SQLAlchemyMapped[list] = sqlalchemy_mapped_column(sqlalchemy.JSON, nullable=False)
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
    scan_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(sqlalchemy.ForeignKey("scan.id"), nullable=False)
    scan = sqlalchemy_relationship("Scan", back_populates="floorplan")
    intersection_point = sqlalchemy_relationship("IntersectionPoint", back_populates="floorplan")

    __mapper_args__ = {"eager_defaults": True}
