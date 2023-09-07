from pydantic import BaseModel
from uuid import UUID
from src.app.enums import OrderStatusEnum


class OrderItem(BaseModel):
    quantity: int
    total_price: int
    product_id: int


class OrderListOut(BaseModel):
    uuid: UUID
    delivery_address: str
    total_price: int
    status: OrderStatusEnum
    order_items: list[OrderItem]
