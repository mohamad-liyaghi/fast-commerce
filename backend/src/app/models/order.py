from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from src.app.enums import OrderStatusEnum


class Order(Base):
    __tablename__ = "orders"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: UUID = Column(UUID(as_uuid=True), default=uuid4, unique=True)

    delivery_address = Column(String(120), nullable=False)
    total_price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(30), default=OrderStatusEnum.PENDING_PAYMENT)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.title}>"
