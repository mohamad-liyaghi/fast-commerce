from uuid import UUID
from src.app.schemas.base import CartBase


class CartAddIn(CartBase):
    product_uuid: UUID


class CartUpdateIn(CartBase):
    pass
