from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.sql import UUIDType
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from src.app.enums import OrderItemStatusEnum


class OrderItem(Base):
    __tablename__ = "order_items"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: UUIDType = Column(UUIDType, default=uuid4, unique=True)

    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    total_price = Column(Integer, nullable=False)
    status = Column(Enum(OrderItemStatusEnum), default=OrderItemStatusEnum.PREPARING)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="order_items")

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="order_items")

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor = relationship("Vendor", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.order_id} {self.product_id}>"
