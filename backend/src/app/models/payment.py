from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from src.core.sql import UUIDType
from src.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: UUIDType = Column(UUIDType, default=uuid4, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    amount = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="payments")

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.amount} {self.order_id} {self.user_id}>"
