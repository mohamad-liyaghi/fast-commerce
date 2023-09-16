import json
from typing import List
from .base import BaseRepository
from src.core.exceptions import ProductNotFound
from src.app.enums import OrderItemStatusEnum
from src.core.exceptions import (
    AdminRequiredException,
    VendorRequiredException,
    InappropriateOrderStatus,
)
from src.app.models import User, OrderItem


class OrderItemRepository(BaseRepository):
    """
    OrderItem Repository is responsible for handling all the database related
    operations for the order items.
    """

    async def create_order_items(self, order, cart, product_controller):
        """
        Bulk create order items for an order
        """
        product_uuids = list(cart.keys())
        products = await product_controller.retrieve(_in=True, uuid=product_uuids)

        if not products:
            raise ProductNotFound

        # Create a dictionary with product UUIDs and quantities
        quantities = await self._get_quantity(products, cart)

        # Bulk insert the order items
        order_items = await self._bulk_create_items(products, order, quantities)
        return order_items

    @staticmethod
    async def _get_quantity(products, cart) -> dict:
        """return a dict with product UUIDs and quantities"""
        quantities = {
            str(product.uuid): json.loads(cart.get(str(product.uuid))).get("quantity")
            for product in products
        }
        return quantities

    async def _bulk_create_items(self, products, order, quantities) -> List[OrderItem]:
        """Bulk create order items of a cart for an order"""
        order_items = await self.bulk_create(
            [
                self.model(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantities[str(product.uuid)],
                    total_price=product.price * quantities[str(product.uuid)],
                    vendor_id=product.vendor_id,
                )
                for product in products
            ]
        )
        return order_items

    async def set_delivering(
        self, order_item: OrderItem, request_user: User
    ) -> OrderItem:
        """
        Set order item status to DELIVERING [only by its product vendor]
        """
        if request_user.id != order_item.vendor.owner_id:
            raise VendorRequiredException

        if order_item.status != OrderItemStatusEnum.PREPARING:
            raise InappropriateOrderStatus

        return await self.update(
            instance=order_item, status=OrderItemStatusEnum.DELIVERING
        )

    async def set_delivered(
        self, order_item: OrderItem, request_user: User
    ) -> OrderItem:
        """
        Set order item status to DELIVERED [only by admin]
        """
        if not request_user.is_admin:
            raise AdminRequiredException

        if order_item.status != OrderItemStatusEnum.DELIVERING:
            raise InappropriateOrderStatus

        return await self.update(
            instance=order_item, status=OrderItemStatusEnum.DELIVERED
        )
