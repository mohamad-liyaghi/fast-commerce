from datetime import datetime
from typing import Optional, List
from src.app.schemas.base import VendorBaseOut


class VendorCreateOut(VendorBaseOut):
    pass


class VendorUpdateOut(VendorBaseOut):
    pass


class VendorRetrieveOut(VendorBaseOut):
    reviewed_at: Optional[datetime] = None
    owner_id: int
    reviewer_id: Optional[int] = None  # TODO: Make this nested


class VendorUpdateStatusOut(VendorBaseOut):
    pass


VendorListOut = List[VendorRetrieveOut]
