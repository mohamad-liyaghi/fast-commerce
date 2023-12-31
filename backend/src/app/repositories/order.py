from src.core.utils import format_key
from src.core.configs import settings
from .base import BaseRepository
from src.core.exceptions import CartEmptyException, OrderAlreadyPaid, OrderInvalidStatus
from src.app.enums import OrderStatusEnum
from src.app.models import Order


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
    ) -> Order:
        """Create a order with its item from a cart."""
        if not cart:
            raise CartEmptyException

        order = await self.create(total_price=9999, **data)
        order_items = await self._create_cart_items(
            order=order,
            cart=cart,
            order_item_controller=order_item_controller,
            product_controller=product_controller,
        )
        await self._delete_cart(cart_controller, data.get("user"))
        total_price = sum(item.total_price for item in order_items)
        return await self.update(order, total_price=total_price)

    async def set_paid(self, order: Order) -> Order:
        if order.status != OrderStatusEnum.PENDING_PAYMENT:
            raise OrderAlreadyPaid
        return await self.update(order, status=OrderStatusEnum.PREPARING)

    async def set_delivering(self, order: Order) -> Order:
        if order.status != OrderStatusEnum.PREPARING:
            raise OrderInvalidStatus("Order must be in PREPARING status")

        return await self.update(order, status=OrderStatusEnum.DELIVERING)

    async def set_delivered(self, order: Order) -> Order:
        if order.status != OrderStatusEnum.DELIVERING:
            raise OrderInvalidStatus("Order must be in DELIVERING status")
        return await self.update(order, status=OrderStatusEnum.DELIVERED)

    @staticmethod
    async def _delete_cart(cart_controller, user):
        cache_key = await format_key(key=settings.CACHE_CART_KEY, user_uuid=user.uuid)
        await cart_controller.delete_cache(key=cache_key)

    @staticmethod
    async def _create_cart_items(
        order: Order, cart: dict, order_item_controller, product_controller
    ):
        order_items = await order_item_controller.create_order_items(
            order=order,
            cart=cart,
            product_controller=product_controller,
        )
        return order_items
