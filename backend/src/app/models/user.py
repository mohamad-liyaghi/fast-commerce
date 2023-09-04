from sqlalchemy import Column, Integer, String, Boolean, DateTime, UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from typing import Optional
from datetime import datetime
from src.core.database import Base
from .vendor import Vendor  # noqa: F401


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    uuid: UUID = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    email: str = Column(String, unique=True, index=True)
    first_name: str = Column(String(25), nullable=False)
    last_name: Optional[str] = Column(String(25), nullable=True)
    is_admin: bool = Column(Boolean, default=False)
    date_joined: datetime = Column(DateTime, default=datetime.utcnow)
    password: str = Column(String)

    vendors = relationship(
        "Vendor",
        back_populates="owner",
        foreign_keys="Vendor.owner_id",
    )
    approved_vendors = relationship(
        "Vendor", back_populates="reviewer", foreign_keys="Vendor.reviewer_id"
    )
    products = relationship(
        "Product",
        back_populates="user",
        foreign_keys="Product.user_id",
    )

    def __repr__(self):
        return f"<User {self.email}>"
