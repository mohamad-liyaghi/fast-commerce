from fastapi import HTTPException, status
from uuid import UUID
from src.app.controllers.base import BaseController
from src.app.models import User, Order
from src.core.exceptions import CartEmptyException, OrderAlreadyPaid, OrderInvalidStatus
from src.app.enums import OrderStatusEnum


class OrderController(BaseController):
    """
    Order Controller is responsible for handling all the database related
    operations for the orders.
    """

    async def create_order(
        self,
        request_user: User,
        order_item_controller,
        cart_controller,
        product_controller,
        cart: dict,
        **data,
    ):
        data["user"] = request_user
        try:
            return await self.repository.create_order(
                order_item_controller=order_item_controller,
                cart_controller=cart_controller,
                product_controller=product_controller,
                cart=cart,
                **data,
            )
        except CartEmptyException:
            raise HTTPException(
                detail="Cart must not be empty", status_code=status.HTTP_400_BAD_REQUEST
            )

    async def update_status(self, order_uuid: UUID, request_user: User, **data):
        order = await self.get_by_uuid(uuid=order_uuid)

        match data.get("status"):
            case OrderStatusEnum.DELIVERING:
                return await self.set_delivering(order=order, request_user=request_user)

            case OrderStatusEnum.DELIVERED:
                return await self.set_delivered(order=order, request_user=request_user)

            case _:
                raise HTTPException(
                    detail="Invalid order status",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

    async def set_paid(self, order: Order):  # TODO: add this to updapte status
        try:
            return await self.repository.set_paid(order=order)
        except OrderAlreadyPaid:
            raise HTTPException(
                detail="Order already paid", status_code=status.HTTP_400_BAD_REQUEST
            )

    async def set_delivering(self, order: Order, request_user: User) -> Order:
        if request_user.is_admin:
            try:
                return await self.repository.set_delivering(order=order)
            except OrderInvalidStatus:
                raise HTTPException(
                    detail="Order must be in paid first status",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        raise HTTPException(
            detail="You don't have permission to perform this action",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    async def set_delivered(self, order: Order, request_user: User) -> Order:
        if request_user.id == order.user_id:
            try:
                return await self.repository.set_delivered(order=order)
            except OrderInvalidStatus:
                raise HTTPException(
                    detail="Order must be in delivering status",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        raise HTTPException(
            detail="You don't have permission to perform this action",
            status_code=status.HTTP_403_FORBIDDEN,
        )
