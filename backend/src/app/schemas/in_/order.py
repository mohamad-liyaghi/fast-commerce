from pydantic import BaseModel
from src.app.schemas.base import OrderBase
from src.app.enums import OrderStatusEnum


class OrderCreateIn(OrderBase):
    pass


class OrderStatusIn(BaseModel):
    status: OrderStatusEnum
