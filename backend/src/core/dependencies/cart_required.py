from fastapi import status, HTTPException, Depends
from .authentication import AuthenticationRequired
from src.core.utils import format_key
from src.app.models import User
from src.core.configs import settings
from src.app.controllers import CartController
from src.core.factory import Factory


class CartRequired:
    """
    Make sure that user has a cart and it is not empty
    """

    async def __call__(
        self,
        user: User = Depends(AuthenticationRequired()),
        cart_controller: CartController = Depends(Factory.get_cart_controller),
    ) -> None:
        key = await format_key(key=settings.CACHE_CART_KEY, user_uuid=user.uuid)
        cart = await cart_controller.get_cache(key=key)

        if not cart:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty",
            )
