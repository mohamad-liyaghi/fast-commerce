from pydantic import BaseModel, Field
from uuid import UUID


class CartAddIn(BaseModel):
    product_uuid: UUID
    quantity: int = Field(1, ge=1, le=10)
