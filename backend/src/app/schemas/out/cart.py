from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ItemMetaData(BaseModel):
    quantity: int
    created_at: datetime


class CartListOut(BaseModel):
    product_uuid: UUID | str
    metadata: ItemMetaData
