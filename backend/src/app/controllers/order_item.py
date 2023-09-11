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

    async def create_order_items(
        self, order, cart, product_controller
    ) -> List[OrderItem]:
        """
        Create order items from a cart and associate them with an order
        """
        return await self.repository.create_order_items(
            order=order, cart=cart, product_controller=product_controller
        )

    async def get_preparing_items(
        self, vendor: Vendor, order_controller: OrderController
    ) -> Optional[List[OrderItem]]:
        """
        Get all the order items of the vendor
        Which the order is paid and the order item is preparing
        """

        preparing_orders = await order_controller.retrieve(
            status=OrderStatusEnum.PREPARING, many=True
        )

        if preparing_orders:
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
        """
        Update status of an order item
        Vendor can set status to DELIVERING
        Admin can set status to DELIVERED
        """
        order_item = await self.get_by_uuid(
            uuid=order_item_uuid, join_fields=["vendor"]
        )

        match status:
            case OrderItemStatusEnum.DELIVERING:
                await self.set_delivering(
                    order_item=order_item, request_user=request_user
                )
            case OrderItemStatusEnum.DELIVERED:
                await self.set_delivered(
                    order_item=order_item, request_user=request_user
                )
            case _:
                raise HTTPException(
                    status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                    detail="Invalid status",
                )

    async def set_delivering(
        self, order_item: OrderItem, request_user: User
    ) -> OrderItem:
        """
                Set order item status to DELIVERING.
        Only vendor can set order item status to DELIVERING
        """
        try:
            return await self.repository.set_delivering(
                order_item=order_item, request_user=request_user
            )
        except VendorRequiredException:
            raise HTTPException(
                status_code=fastapi_status.HTTP_403_FORBIDDEN,
                detail="Only vendor can set order item status to DELIVERING",
            )
        except InappropriateOrderStatus:
            raise HTTPException(
                status_code=fastapi_status.HTTP_400_BAD_REQUEST,
                detail="Order status should be PREPARING",
            )

    async def set_delivered(
        self, order_item: OrderItem, request_user: User
    ) -> OrderItem:
        """
        Set order item status to DELIVERED.
        Only admin can set order item status to DELIVERED
        """
        try:
            return await self.repository.set_delivered(
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

    async def get_order_item(self, request_user: User, uuid: UUID) -> OrderItem:
        """
        Retrieve an order item by uuid
        Only admin, vendor [of the product] and order user can retrieve an order item.
        """
        item = await self.get_by_uuid(
            uuid=uuid, join_fields=["vendor", "order", "product"]
        )

        if (
            request_user.is_admin
            or request_user.id == item.vendor.owner_id
            or request_user.id == item.order.user_id
        ):
            return item

        raise HTTPException(
            status_code=fastapi_status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this order item",
        )
