from src.app.repositories.base import BaseRepository
from src.app.models import User, Vendor, VendorStatus, Product
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

        if not request_vendor.status == VendorStatus.ACCEPTED:
            raise AcceptedVendorRequired

        return await super().create(**data)

    async def update(
        self, instance: Product, request_user: User, data: dict
    ) -> Product:
        await self._check_owner(instance, request_user)
        return await super().update(instance, **data)

    async def delete(self, instance: Product, request_user: User):
        await self._check_owner(instance, request_user)
        return await super().delete(instance)

    @staticmethod
    async def _check_owner(product, request_user):
        """Make sure the request user is the owner of the product."""
        if product.user_id != request_user.id:
            raise ProductOwnerRequired
