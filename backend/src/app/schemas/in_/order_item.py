from pydantic import BaseModel
from src.app.enums import OrderItemStatusEnum


class OrderItemStatusIn(BaseModel):
    status: OrderItemStatusEnum
