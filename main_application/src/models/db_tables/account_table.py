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


class Account(DBBaseTable):
    __tablename__ = "account"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True, autoincrement="auto"
    )
    username: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    email: SQLAlchemyMapped[pydantic.EmailStr] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    password: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=64), nullable=False
    )
    is_admin: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean, default=False
    )
    is_logged_in: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean, default=True
    )
    is_verified: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean, default=False
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

    __mapper_args__ = {"eager_defaults": True}
