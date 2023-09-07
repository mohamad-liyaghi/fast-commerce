from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.sql import UUIDType
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from src.app.enums import OrderStatusEnum
from .order_item import OrderItem  # noqa: F401


class Order(Base):
    __tablename__ = "orders"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: UUIDType = Column(UUIDType, default=uuid4, unique=True)

    delivery_address = Column(String(120), nullable=False)
    total_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING_PAYMENT)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order {self.delivery_address}>"
