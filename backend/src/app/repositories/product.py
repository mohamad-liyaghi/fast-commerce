from src.app.repositories.base import BaseRepository
from src.app.models import User, Vendor, Product
from src.app.enums import VendorStatusEnum
from src.core.exceptions import ProductOwnerRequired, AcceptedVendorRequired


class ProductRepository(BaseRepository):
    """
    Product Repository is responsible for all db operations of a product
    """

    async def create(
        self, request_user: User, request_vendor: Vendor, **data: dict
    ) -> Product:
        data.setdefault("vendor_id", request_vendor.id)
        data.setdefault("user_id", request_user.id)

        if not request_vendor.status == VendorStatusEnum.ACCEPTED:
            raise AcceptedVendorRequired

        return await super().create(**data)

    async def update_product(
        self, instance: Product, request_user: User, data: dict
    ) -> Product:
        await self._check_product_owner(instance, request_user)
        return await super().update(instance, **data)

    async def delete_product(self, instance: Product, request_user: User):
        await self._check_product_owner(instance, request_user)
        return await super().delete(instance)

    @staticmethod
    async def _check_product_owner(product, request_user) -> None:
        """Make sure the request user is the owner of the product."""
        if product.user_id != request_user.id:
            raise ProductOwnerRequired
