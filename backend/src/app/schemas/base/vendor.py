from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from src.app.enums import VendorStatusEnum


class VendorBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=300)
    domain: str = Field(min_length=3, max_length=50)
    address: str = Field(min_length=3, max_length=150)


class VendorBaseOut(VendorBase):
    uuid: UUID | str
    status: VendorStatusEnum
    created_at: datetime
