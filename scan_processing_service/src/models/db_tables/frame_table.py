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


class Frame(DBBaseTable):
    __tablename__ = "frame"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True, autoincrement="auto"
    )
    frame_index: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
    projection_matrix: SQLAlchemyMapped[list] = sqlalchemy_mapped_column(
        sqlalchemy.JSON, nullable=False
    )
    camera_pose_ar_frame: SQLAlchemyMapped[list] = sqlalchemy_mapped_column(
        sqlalchemy.JSON, nullable=False
    )
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
    scan_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        sqlalchemy.ForeignKey("scan.id"), nullable=False
    )
    scan = sqlalchemy_relationship("Scan", back_populates="frame")

    __mapper_args__ = {"eager_defaults": True}
