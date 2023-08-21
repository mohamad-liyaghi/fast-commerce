from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr = Field(example="user@email.com")
    first_name: str = Field(example="John")
    last_name: str = Field(example="Doe")


class CurrentUser(BaseModel):
    uuid: UUID = Field(None, description="User UUID")

    class Config:
        validate_assignment = True
