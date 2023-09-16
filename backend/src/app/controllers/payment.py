from uuid import UUID
from src.app.controllers.base import BaseController
from src.app.models import Order, Payment, User
from src.app.controllers import OrderController


class PaymentController(BaseController):
    """
    Payment Controller is responsible for handling all the payment related
    operations.
    """

    async def pay_order(
        self, request_user: User, order_uuid: UUID, order_controller: OrderController
    ) -> Payment:
        """
        Pay Order is responsible for handling the payment of an order.
        """
        order: Order = await order_controller.get_by_uuid(
            uuid=order_uuid, user_id=request_user.id
        )
        payment: Payment = await self.create(
            user=request_user,
            order=order,
            amount=order.total_price,
        )
        await order_controller._set_paid(order=order)
        return payment
