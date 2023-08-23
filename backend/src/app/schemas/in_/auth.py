from pydantic import Field
from src.app.schemas.base import UserBase, UserBaseEmail, UserBasePassword


class UserRegisterIn(UserBase):
    password: str = Field(example="STRONG_password1234$$")


class UserVerifyIn(UserBaseEmail):
    otp: int = Field(example=12345, ge=10000, le=99999)


class UserLoginIn(UserBaseEmail, UserBasePassword):
    password: str = Field(example="STRONG_password1234$$")
