from pydantic import BaseModel
from uuid import UUID
from typing import List
from src.app.enums import OrderStatusEnum


class OrderItem(BaseModel):
    quantity: int
    total_price: int
    uuid: UUID


class OrderRetrieveOut(BaseModel):
    order_items: List[OrderItem]


class OrderListOut(BaseModel):
    uuid: UUID
    delivery_address: str
    total_price: int
    status: OrderStatusEnum
    order_items: list[OrderItem]
