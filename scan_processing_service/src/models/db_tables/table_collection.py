"""
This file is neccessary for the initialization of the database tables.
All database tables should be imported here, else they will not be initialized.
"""

from src.models.db_tables.floorplan_table import Floorplan
from src.models.db_tables.frame_table import Frame
from src.models.db_tables.intersection_point_table import IntersectionPoint
from src.models.db_tables.scan_table import Scan
from src.utility.database.base_table import DBBaseTable
