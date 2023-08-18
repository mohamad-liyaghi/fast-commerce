from pydantic import Field, EmailStr, BaseModel
from src.app.schemas.base import UserBase


class UserRegisterIn(UserBase):
    password: str = Field(example="STRONG_password1234$$")


class UserVerifyIn(BaseModel):
    email: EmailStr = Field(example="user@email.com")
    otp: int = Field(example=12345, ge=10000, le=99999)
