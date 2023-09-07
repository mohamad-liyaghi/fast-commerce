from src.app.controllers.base import BaseController


class OrderItemController(BaseController):
    """
    OrderItem Controller is responsible for handling all the database related
    operations for the Order items.
    """

    async def create_order_items(self, order, cart, product_controller):
        return await self.repository.create_order_items(
            order=order, cart=cart, product_controller=product_controller
        )
