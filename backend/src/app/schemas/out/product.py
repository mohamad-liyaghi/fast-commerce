from datetime import datetime
from uuid import UUID
from src.app.schemas.out import UserOut
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
    user: UserOut


class ProductListOut(BaseProduct):
    uuid: UUID
