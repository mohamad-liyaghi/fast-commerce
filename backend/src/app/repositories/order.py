from src.core.utils import format_key
from src.core.configs import settings
from .base import BaseRepository
from src.core.exceptions import CartEmptyException


class OrderRepository(BaseRepository):
    """
    Order Repository is responsible for handling all the database related
    operations for the orders.
    """

    async def create_order(
        self,
        order_item_controller,
        cart_controller,
        product_controller,
        cart: dict,
        **data
    ):
        if not cart:
            raise CartEmptyException

        order = await self.create(total_price=0, **data)

        # Create order items and update the total price
        order_items = await order_item_controller.create_order_items(
            order=order,
            cart=cart,
            product_controller=product_controller,
        )
        await self._delete_cart(cart_controller, data.get("user"))
        # Update total price
        total_price = sum(item.total_price for item in order_items)
        return await self.update(order, total_price=total_price)

    @staticmethod
    async def _delete_cart(cart_controller, user):
        cache_key = await format_key(key=settings.CACHE_CART_KEY, user_uuid=user.uuid)
        await cart_controller.delete_cache(key=cache_key)
