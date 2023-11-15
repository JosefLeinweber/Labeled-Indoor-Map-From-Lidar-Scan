import datetime
import loguru
import pydantic
from password_strength import PasswordPolicy

from src.utility.pydantic_schema.base_schema import BaseModel


class AccountBase(BaseModel):
    username: str
    email: pydantic.EmailStr


class AccountInAuthentication(AccountBase):
    password: str

    @pydantic.validator("password")
    def password_strength(cls, v):
        loguru.logger.info("Evaluating password strength")
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
        )
        if policy.test(v) != []:
            raise ValueError("Password is not strong enough")
        return v


class AccountInUpdate(AccountBase):
    username: str | None
    email: pydantic.EmailStr | None
    password: str | None


class AccountOut(AccountBase):
    id: int | None
    username: str
    email: pydantic.EmailStr
    password: str | None
    is_admin: bool | None
    is_logged_in: bool | None
    is_verified: bool | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None


class AccountOutDelete(BaseModel):
    is_deleted: bool
