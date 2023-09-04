from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from src.core.database import Base
from .product import Product  # noqa: F401
from src.app.enums import VendorStatusEnum


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True)

    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    domain = Column(String(50), nullable=True)
    address = Column(String(150), nullable=False)

    status = Column(Enum(VendorStatusEnum), default=VendorStatusEnum.PENDING)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship(
        "User",
        back_populates="vendors",
        foreign_keys=[owner_id],
    )
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewer = relationship(
        "User",
        back_populates="approved_vendors",
        foreign_keys=[reviewer_id],
    )
    products = relationship("Product", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor {self.name}>"
