from datetime import datetime
from uuid import UUID
from src.app.schemas.out import ProfileOut
from src.app.schemas.base import BaseProductSpecs, BaseProduct, VendorBaseOut


class ProductCreateOut(BaseProductSpecs):
    uuid: UUID
    created_at: datetime


class ProductUpdateOut(BaseProductSpecs):
    uuid: UUID


class ProductRetrieveOut(BaseProductSpecs):
    uuid: UUID
    created_at: datetime
    vendor: VendorBaseOut
    user: ProfileOut


class ProductListOut(BaseProduct):
    uuid: UUID
