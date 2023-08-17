from pydantic import Field
from src.app.schemas.base import UserBase


class UserRegisterIn(UserBase):
    password: str = Field(example="STRONG_password1234$$")
