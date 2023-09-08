from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired, VendorRequired
from src.app.controllers import OrderController, PaymentController


router = APIRouter(
    tags=["Payment"],
)


@router.post("/{order_uuid}", status_code=status.HTTP_200_OK)
async def pay_order(
    order_uuid: UUID,
    current_user: dict = Depends(AuthenticationRequired()),
    payment_controller: PaymentController = Depends(Factory.get_payment_controller),
    order_controller: OrderController = Depends(Factory.get_order_controller),
):
    return await payment_controller.pay_order(
        request_user=current_user,
        order_uuid=order_uuid,
        order_controller=order_controller,
    )
