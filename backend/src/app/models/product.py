from sqlalchemy import Column, Integer, String, DateTime, UUID, JSON, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from .order_item import OrderItem  # noqa: F401
from src.core.utils import generate_uuid


class Product(Base):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: str = Column(String(36), default=generate_uuid, unique=True)

    title = Column(String(120), nullable=False)
    description = Column(String(300), nullable=False)
    price = Column(Integer, nullable=False)
    specs = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    vendor = relationship("Vendor", back_populates="products")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="products")

    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.title}>"
