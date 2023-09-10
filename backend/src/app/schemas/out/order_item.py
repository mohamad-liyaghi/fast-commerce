from pydantic import BaseModel
from uuid import UUID


class OrderItemProduct(BaseModel):
    uuid: UUID


class OrderItemList(BaseModel):
    uuid: UUID
    product: OrderItemProduct
    quantity: int
    total_price: int
