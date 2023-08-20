from pydantic import BaseModel, Field


class ProfileUpdateIn(BaseModel):
    first_name: str = Field(None, min_length=1, max_length=50)
    last_name: str = Field(None, min_length=1, max_length=50)
