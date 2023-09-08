from fastapi import HTTPException, status
from src.app.controllers.base import BaseController
from src.app.models import User, Order
from src.core.exceptions import CartEmptyException, OrderAlreadyPaid


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
        **data
    ):
        data["user"] = request_user
        try:
            return await self.repository.create_order(
                order_item_controller=order_item_controller,
                cart_controller=cart_controller,
                product_controller=product_controller,
                cart=cart,
                **data
            )
        except CartEmptyException:
            raise HTTPException(
                detail="Cart must not be empty", status_code=status.HTTP_400_BAD_REQUEST
            )

    async def set_paid(self, order: Order):
        try:
            return await self.repository.set_paid(order=order)
        except OrderAlreadyPaid:
            raise HTTPException(
                detail="Order already paid", status_code=status.HTTP_400_BAD_REQUEST
            )
