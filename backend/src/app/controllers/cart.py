from fastapi import HTTPException, status
import json
from typing import Optional, List
from src.core.utils import format_key
from src.app.schemas.out import CartListOut
from src.app.controllers.base import BaseController
from src.app.controllers import ProductController
from src.app.models import User
from src.core.configs import settings


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
        # Get the product, if not exist raise 404
        product = await product_controller.get_by_uuid(uuid=kwargs.get("product_uuid"))

        # Product user cannot add its own product to cart
        if product.user_id == request_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't add your own product to cart",
            )

        cache_key = await format_key(
            key=settings.CACHE_CART_KEY, user_uuid=request_user.uuid
        )

        cart_product = await self.get_cache(key=cache_key, field=str(product.uuid))

        if cart_product:
            # Increase the quantity of the product if already exist
            cart_product = json.loads(cart_product)
            cart_product["quantity"] += kwargs.get("quantity")
            await self.create_cache(
                key=cache_key, data={str(product.uuid): json.dumps(cart_product)}
            )
        else:
            # Create a new cart product if not exist
            cart_product = {"quantity": kwargs.get("quantity")}
            await self.create_cache(
                key=cache_key, data={str(product.uuid): json.dumps(cart_product)}
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
