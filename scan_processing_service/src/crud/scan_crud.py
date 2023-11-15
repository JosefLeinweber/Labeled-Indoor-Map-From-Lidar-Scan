from src.models.db_tables.scan_table import Scan
from src.models.schemas.scan_schema import ScanInCreate, ScanOutDelete, ScanOut
import sqlalchemy
import loguru
import fastapi
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import exc as sqlalchemy_error


async def create(scan: ScanInCreate, db_session) -> Scan:
    loguru.logger.info("* creating new scan")
    new_scan = Scan(**scan.model_dump())
    db_session.add(instance=new_scan)
    await db_session.commit()
    await db_session.refresh(instance=new_scan)
    await db_session.close()
    return new_scan


async def get_by_id(id: int, db_session) -> ScanOut:
    loguru.logger.info("* getting scan by id")
    select_stmt = (
        sqlalchemy.select(Scan)
        .options(sqlalchemy_selectinload("*"))
        .where(Scan.id == id)
    )
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().first()


async def delete_by_id(id: int, db_session) -> ScanOutDelete:
    loguru.logger.info("* deleting scan by id")
    scan_to_delete = await get_by_id(id=id, db_session=db_session)
    if not scan_to_delete:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Scan with id {id} not found"
        )
    delete_stmt = sqlalchemy.delete(Scan).where(Scan.id == id)

    try:
        await db_session.execute(statement=delete_stmt)
        await db_session.commit()
        await db_session.close()
        return ScanOutDelete(**scan_to_delete.model_dump(), is_deleted=True)

    except sqlalchemy_error.DatabaseError as e:
        await db_session.rollback()
        await db_session.close()
        raise fastapi.HTTPException(status_code=500, detail=f"Database error: {e}")


#! Only for development!
async def get_all(db_session) -> list[ScanOut]:
    loguru.logger.info("* getting all scans")
    select_stmt = sqlalchemy.select(Scan).options(sqlalchemy_selectinload("*"))
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().all()
