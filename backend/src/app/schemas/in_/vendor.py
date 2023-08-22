from pydantic import BaseModel
from src.app.schemas.base import VendorBase
from src.app.models import VendorStatus


class VendorCreateIn(VendorBase):
    pass


class VendorUpdateStatusIn(BaseModel):
    status: VendorStatus
