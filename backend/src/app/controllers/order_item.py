from typing import List, Optional
from src.app.controllers.base import BaseController
from src.app.enums import OrderStatusEnum, OrderItemStatusEnum
from src.app.models import Vendor, OrderItem
from src.app.controllers import OrderController


class OrderItemController(BaseController):
    """
    OrderItem Controller is responsible for handling all the database related
    operations for the Order items.
    """

    async def create_order_items(self, order, cart, product_controller):
        return await self.repository.create_order_items(
            order=order, cart=cart, product_controller=product_controller
        )

    async def get_preparing(
        self, vendor: Vendor, order_controller: OrderController
    ) -> Optional[List[OrderItem]]:
        # Get all orders with status of PREPARING
        # Which means they are paid
        preparing_orders = await order_controller.retrieve(
            status=OrderStatusEnum.PREPARING, many=True
        )

        if preparing_orders:
            # Return order items of the vendor
            # Which the order is paid and the order item is preparing
            return await self.retrieve(
                join_fields=["order", "product"],
                _in=True,
                order_id=[order.id for order in preparing_orders],
                vendor_id=[vendor.id],
                status=[OrderItemStatusEnum.PREPARING],
                many=True,
            )
