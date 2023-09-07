from pydantic import BaseModel, Field
from datetime import datetime
from src.app.enums import VendorStatusEnum
from uuid import UUID


class VendorBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=300)
    domain: str = Field(min_length=3, max_length=50)
    address: str = Field(min_length=3, max_length=150)


class VendorBaseOut(VendorBase):
    uuid: UUID
    status: VendorStatusEnum
    created_at: datetime
