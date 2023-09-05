from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from src.app.enums import OrderItemStatusEnum
from src.core.utils import generate_uuid


class OrderItem(Base):
    __tablename__ = "order_items"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: str = Column(String(36), default=generate_uuid, unique=True)

    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    total_price = Column(Integer, nullable=False)
    status = Column(String(30), default=OrderItemStatusEnum.PENDING_PAYMENT)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="order_items")

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product = relationship("Product", back_populates="order_items")

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor = relationship("Vendor", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.title}>"
