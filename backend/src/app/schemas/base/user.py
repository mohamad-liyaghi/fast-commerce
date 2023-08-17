from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(example="user@email.com")
    first_name: str = Field(example="John")
    last_name: str = Field(example="Doe")
