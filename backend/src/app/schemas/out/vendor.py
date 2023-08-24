from datetime import datetime
from typing import Optional, List
from src.app.schemas.base import VendorBaseOut, UserBase


class VendorCreateOut(VendorBaseOut):
    pass


class VendorUpdateOut(VendorBaseOut):
    pass


class VendorRetrieveOut(VendorBaseOut):
    reviewed_at: Optional[datetime] = None
    owner: UserBase
    reviewer: Optional[UserBase] = None


class VendorUpdateStatusOut(VendorBaseOut):
    pass


VendorListOut = List[VendorRetrieveOut]
