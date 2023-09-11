from fastapi import HTTPException, status as fastapi_status
from typing import List, Optional
from uuid import UUID
from src.app.controllers.base import BaseController
from src.app.enums import OrderStatusEnum, OrderItemStatusEnum
from src.app.models import Vendor, OrderItem, User
from src.app.controllers import OrderController
from src.core.exceptions import (
    AdminRequiredException,
    VendorRequiredException,
    InappropriateOrderStatus,
)


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
                join_fields=["product"],
                _in=True,
                order_id=[order.id for order in preparing_orders],
                vendor_id=[vendor.id],
                status=[OrderItemStatusEnum.PREPARING],
                many=True,
            )

    async def update_status(
        self, order_item_uuid: UUID, status: OrderItemStatusEnum, request_user: User
    ):
        order_item = await self.get_by_uuid(
            uuid=order_item_uuid, join_fields=["vendor"]
        )

        match status:
            case OrderItemStatusEnum.DELIVERING:
                try:
                    await self.repository.set_delivering(
                        order_item=order_item, request_user=request_user
                    )
                except VendorRequiredException:
                    raise HTTPException(
                        status_code=fastapi_status.HTTP_403_FORBIDDEN,
                        detail="Only product vendor can set order item status to DELIVERING",
                    )
                except InappropriateOrderStatus:
                    raise HTTPException(
                        status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                        detail="Order status should be PREPARING",
                    )

            case OrderItemStatusEnum.DELIVERED:
                try:
                    await self.repository.set_delivered(
                        order_item=order_item, request_user=request_user
                    )
                except AdminRequiredException:
                    raise HTTPException(
                        status_code=fastapi_status.HTTP_403_FORBIDDEN,
                        detail="Only admin can set order item status to DELIVERED",
                    )
                except InappropriateOrderStatus:
                    raise HTTPException(
                        status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                        detail="Order status should be DELIVERING",
                    )

            case _:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                    detail="Invalid status",
                )
