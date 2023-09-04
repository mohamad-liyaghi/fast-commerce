from pydantic import BaseModel
from src.app.schemas.base import VendorBase
from src.app.enums import VendorStatusEnum


class VendorCreateIn(VendorBase):
    pass


class VendorUpdateIn(VendorBase):
    pass


class VendorUpdateStatusIn(BaseModel):
    status: VendorStatusEnum
