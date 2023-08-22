from pydantic import BaseModel, Field


class VendorCreateIn(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=300)
    domain: str = Field(min_length=3, max_length=50)
    address: str = Field(min_length=3, max_length=150)
