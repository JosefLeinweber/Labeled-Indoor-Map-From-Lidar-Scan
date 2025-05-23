import datetime

import pydantic
import sqlalchemy
from sqlalchemy import PickleType as PickleTypeForDict
from sqlalchemy.orm import (
    Mapped as SQLAlchemyMapped,
    mapped_column as sqlalchemy_mapped_column,
    relationship as sqlalchemy_relationship,
)
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.utility.database.base_table import DBBaseTable


class Scan(DBBaseTable):
    __tablename__ = "scan"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=False)
    user_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
    num_images: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
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
    frame = sqlalchemy_relationship("Frame", back_populates="scan")
    floorplan = sqlalchemy_relationship("Floorplan", back_populates="scan")

    __mapper_args__ = {"eager_defaults": True}
