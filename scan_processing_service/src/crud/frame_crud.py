from src.models.db_tables.frame_table import Frame
from src.models.schemas.frame_schema import FrameInCreate, FrameOutDelete, FrameOut
from src.models.schemas.scan_schema import ScanOut
import sqlalchemy
import loguru
import fastapi
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import exc as sqlalchemy_error


async def create(frame: FrameInCreate, parent_scan: ScanOut, db_session) -> Frame:
    loguru.logger.info("* creating new frame")
    new_frame = Frame(**frame.model_dump())
    new_frame.scan = parent_scan
    db_session.add(instance=new_frame)
    await db_session.commit()
    await db_session.refresh(instance=new_frame)
    await db_session.close()
    loguru.logger.debug(f"Created frame: {new_frame.__dict__}")
    return new_frame


async def get_by_id(id: int, db_session) -> FrameOut:
    loguru.logger.info("* getting frame by id")
    select_stmt = (
        sqlalchemy.select(Frame)
        .options(sqlalchemy_selectinload("*"))
        .where(Frame.id == id)
    )
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().first()


async def delete_by_id(id: int, db_session) -> FrameOutDelete:
    loguru.logger.info("* deleting frame by id")
    frame_to_delete = await get_by_id(id=id, db_session=db_session)
    if not frame_to_delete:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Frame with id {id} not found"
        )
    delete_stmt = sqlalchemy.delete(Frame).where(Frame.id == id)

    try:
        await db_session.execute(statement=delete_stmt)
        await db_session.commit()
        await db_session.close()
        return FrameOutDelete(**frame_to_delete.model_dump(), is_deleted=True)

    except sqlalchemy_error.DatabaseError as e:
        await db_session.rollback()
        await db_session.close()
        raise fastapi.HTTPException(status_code=500, detail=f"Database error: {e}")


async def get_frames_by_scan_id(scan_id: int, db_session):
    loguru.logger.info("* getting frames by scan id")
    select_stmt = (
        sqlalchemy.select(Frame)
        .options(sqlalchemy_selectinload("*"))
        .where(Frame.scan_id == scan_id)
    )
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().all()


#! Only for development!
async def get_all(db_session) -> list[FrameOut]:
    loguru.logger.info("* getting all frames")
    select_stmt = sqlalchemy.select(Frame).options(sqlalchemy_selectinload("*"))
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().all()
