from datetime import datetime
from src.app.schemas.base import VendorBase
from src.app.models import VendorStatusEnum


class VendorCreateOut(VendorBase):
    status: VendorStatusEnum
    created_at: datetime
