from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ItemMetaData(BaseModel):
    quantity: int
    created_at: datetime


class CartListOut(BaseModel):
    product_uuid: UUID
    metadata: ItemMetaData
