from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class UserBaseEmail(BaseModel):
    email: EmailStr = Field(example="user@email.com", min_length=5, max_length=100)


class UserBasePassword(BaseModel):
    password: str = Field(example="STRONG_password1234$$")


class UserBase(UserBaseEmail):
    first_name: str = Field(example="John")
    last_name: str = Field(example="Doe")


class CurrentUser(BaseModel):
    uuid: UUID = Field(None, description="User UUID")

    class Config:
        validate_assignment: bool = True
