from fastapi import HTTPException, status
import json
from uuid import UUID
from typing import Optional, List
from src.core.utils import format_key
from src.app.schemas.out import CartListOut
from src.app.controllers.base import BaseController
from src.app.controllers import ProductController
from src.app.models import User
from src.core.configs import settings
from src.core.exceptions import (
    CartItemOwnerException,
    CartItemQuantityException,
    CartItemNotFound,
)


class CartController(BaseController):
    """
    This controller is responsible for saving and doing cart related operations in cache
    """

    async def add_item(
        self, product_controller: ProductController, request_user: User, **kwargs
    ) -> None:
        """
        Add a new product to cart
        """
        product = await product_controller.get_by_uuid(uuid=kwargs.get("product_uuid"))

        try:
            await self.repository.add_item(
                product=product, request_user=request_user, **kwargs
            )

        except CartItemOwnerException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't add your own product to cart",
            )
        except CartItemQuantityException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't add more than 10 products to cart",
            )

    async def get_items(self, request_user: User) -> Optional[List[CartListOut]]:
        cache_key = await format_key(
            key=settings.CACHE_CART_KEY, user_uuid=request_user.uuid
        )
        result = await self.get_cache(key=cache_key)

        if result:
            items = [
                CartListOut(
                    product_uuid=product_uuid, metadata=json.loads(product_metadata)
                )
                for product_uuid, product_metadata in result.items()
            ]
            return items

        return

    async def update_item(
        self, request_user: User, product_uuid: UUID | str, **kwargs
    ) -> None:
        """
        Update a product in cart
        """
        try:
            await self.repository.update_item(
                product_uuid=product_uuid, request_user=request_user, **kwargs
            )

        except CartItemNotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in cart",
            )

    async def delete_item(self, request_user: User, product_uuid: UUID | str) -> None:
        """
        Delete a product from cart
        """
        try:
            await self.repository.delete_item(
                product_uuid=product_uuid, request_user=request_user
            )

        except CartItemNotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in cart",
            )
