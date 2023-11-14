"""
This file contains the base table class from which all other database tables should inherit.
"""


import sqlalchemy
from sqlalchemy.orm import DeclarativeBase


class DBBaseTable(DeclarativeBase):
    metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()
