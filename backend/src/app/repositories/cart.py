import json
from datetime import datetime
from uuid import UUID
from .base import BaseCacheRepository
from src.app.models import Product, User
from src.core.exceptions import (
    CartItemOwnerException,
    CartItemQuantityException,
    CartItemNotFound,
)
from src.core.utils import format_key
from src.core.configs import settings


class CartRepository(BaseCacheRepository):
    """
    This repository is responsible for saving and doing cart related operations in cache.
    """

    @staticmethod
    async def _is_product_owner(product: Product, request_user: User) -> None:
        """Raise an exception if the product owner is the same as the request user."""
        if product.user_id == request_user.id:
            raise CartItemOwnerException

    @staticmethod
    async def _create_key(user: User):
        """Create a unique key for each user."""
        return await format_key(key=settings.CACHE_CART_KEY, user_uuid=user.uuid)

    async def _get_cart_item(
        self, request_user: User, field: str, raise_exception: bool = False
    ):
        """Retrieve a specific item from the user's cart."""
        key = await self._create_key(user=request_user)
        cart_item = await self.get_cache(key=key, field=field)

        if not cart_item and raise_exception:
            raise CartItemNotFound

        return cart_item

    async def add_item(self, product: Product, request_user: User, **kwargs):
        """Add an item to the cart or increase its quantity if it already exists."""
        await self._is_product_owner(product=product, request_user=request_user)

        key = await self._create_key(user=request_user)
        cart_product = await self.get_cache(key=key, field=str(product.uuid))
        cart_product = json.loads(cart_product) if cart_product else None

        if cart_product:
            # Increase the quantity of the product if already exist
            cart_product["quantity"] += kwargs.get("quantity")

            if cart_product["quantity"] >= 10:
                raise CartItemQuantityException
        else:
            # Create a new cart product if not exist
            cart_product = {
                "quantity": kwargs.get("quantity"),
                "created_at": str(datetime.now()),
            }

        await self.create_cache(
            key=key,
            data={str(product.uuid): json.dumps(cart_product)},
        )

    async def update_item(
        self, request_user: User, product_uuid: UUID | str, **kwargs
    ) -> None:
        """Update the quantity of a specific item in the cart."""
        product_in_cart = await self._get_cart_item(
            request_user=request_user, field=str(product_uuid), raise_exception=True
        )

        product_in_cart = json.loads(product_in_cart)
        product_in_cart["quantity"] = kwargs.get("quantity")

        key = await self._create_key(user=request_user)
        await self.create_cache(
            key=key, data={str(product_uuid): json.dumps(product_in_cart)}
        )

    async def delete_item(self, request_user: User, product_uuid: UUID | str) -> None:
        """Remove a specific item from the cart."""
        key = await self._create_key(user=request_user)
        await self._get_cart_item(
            request_user=request_user, field=str(product_uuid), raise_exception=True
        )

        await self.delete_cache(key=key, field=str(product_uuid))
