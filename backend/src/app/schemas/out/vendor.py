from datetime import datetime
from typing import Optional
from uuid import UUID
from src.app.schemas.base import VendorBase
from src.app.models import VendorStatus


class VendorCreateOut(VendorBase):
    uuid: UUID
    status: VendorStatus
    created_at: datetime


class VendorRetrieveOut(VendorBase):
    uuid: UUID
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    status: VendorStatus
    owner_id: int
    reviewer_id: Optional[int] = None  # TODO: Make this nested
