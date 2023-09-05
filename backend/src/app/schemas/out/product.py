from uuid import UUID
from datetime import datetime
from src.app.schemas.out import ProfileOut
from src.app.schemas.base import BaseProductSpecs, BaseProduct, VendorBaseOut


class ProductCreateOut(BaseProductSpecs):
    uuid: UUID | str
    created_at: datetime


class ProductUpdateOut(BaseProductSpecs):
    uuid: UUID | str


class ProductRetrieveOut(BaseProductSpecs):
    uuid: UUID | str
    created_at: datetime
    vendor: VendorBaseOut
    user: ProfileOut


class ProductListOut(BaseProduct):
    uuid: UUID | str
