from src.models.db_tables.account_table import Account
from src.models.schemas.account_schema import (
    AccountInAuthentication,
    AccountOut,
    AccountInUpdate,
    AccountOutDelete,
)
import sqlalchemy
import loguru
import fastapi
from sqlalchemy.orm import selectinload as sqlalchemy_selectinload
from sqlalchemy.sql import functions as sqlalchemy_functions
from sqlalchemy import exc as sqlalchemy_error


async def create(account: AccountInAuthentication, db_session) -> Account:
    await check_account_details_are_unique(account=account, db_session=db_session)
    loguru.logger.info("* creating new account")
    new_account = Account(**account.dict())
    db_session.add(instance=new_account)
    await db_session.commit()
    await db_session.refresh(instance=new_account)
    await db_session.close()
    return new_account


async def get_all(db_session) -> list[AccountOut]:
    loguru.logger.info("* getting all accounts")
    select_stmt = sqlalchemy.select(Account).options(sqlalchemy_selectinload("*"))
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().all()


async def get_by_id(id: int, db_session) -> AccountOut:
    loguru.logger.info("* getting account by id")
    select_stmt = (
        sqlalchemy.select(Account)
        .options(sqlalchemy_selectinload("*"))
        .where(Account.id == id)
    )
    query = await db_session.execute(statement=select_stmt)
    await db_session.close()
    return query.scalars().first()


async def update_by_id(id: int, account: AccountInUpdate, db_session) -> AccountOut:
    loguru.logger.info("* updating account by id")
    update_data = account.dict(exclude_unset=True)
    current_account = await get_by_id(id=id, db_session=db_session)
    if not current_account:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Account with id {id} not found"
        )
    update_stmt = (
        sqlalchemy.update(Account)
        .where(Account.id == id)
        .values(updated_at=sqlalchemy_functions.now())
    )

    for key, value in update_data.items():
        update_stmt = update_stmt.values(**{key: value})

    try:
        await db_session.execute(statement=update_stmt)
        await db_session.commit()
        await db_session.refresh(instance=current_account)
        await db_session.close()

        return current_account

    except sqlalchemy_error.DatabaseError as e:
        await db_session.rollback()
        await db_session.close()
        raise fastapi.HTTPException(status_code=500, detail=str(e))


async def delete_by_id(id: int, db_session) -> bool:
    loguru.logger.info("* deleting account by id")
    accout_to_delete = await get_by_id(id=id, db_session=db_session)
    if not accout_to_delete:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Account with id {id} not found"
        )
    delete_stmt = sqlalchemy.delete(Account).where(Account.id == id)
    try:
        await db_session.execute(statement=delete_stmt)
        await db_session.commit()
        await db_session.close()
        return True
    except sqlalchemy_error.DatabaseError as e:
        await db_session.rollback()
        await db_session.close()
        raise fastapi.HTTPException(status_code=500, detail=str(e))


async def check_account_details_are_unique(
    account: AccountInAuthentication, db_session
) -> None:
    loguru.logger.info("* checking if account details are unique")
    email_unique = await _is_email_unique(account.email, db_session)
    username_unique = await _is_username_unique(account.username, db_session)
    await db_session.close()
    if not email_unique:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Email {account.email} already in use"
        )
    if not username_unique:
        raise fastapi.HTTPException(
            status_code=409, detail=f"Username {account.username} already in use"
        )


async def _is_email_unique(email: str, db_session) -> bool:
    loguru.logger.info("* checking if email is unique")
    select_stmt = sqlalchemy.select(Account).where(Account.email == email)
    query = await db_session.execute(statement=select_stmt)
    return query.scalars().first() is None


async def _is_username_unique(username: str, db_session) -> bool:
    loguru.logger.info("* checking if username is unique")
    select_stmt = sqlalchemy.select(Account).where(Account.username == username)
    query = await db_session.execute(statement=select_stmt)
    return query.scalars().first() is None
