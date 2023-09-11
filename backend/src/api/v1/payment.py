from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from typing import List, Optional
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired
from src.app.controllers import OrderController, PaymentController
from src.app.schemas.out import PaymentListOut, PaymentRetrieveOut
from src.app.models import User


router = APIRouter(
    tags=["Payment"],
)


@router.post("/{order_uuid}", status_code=status.HTTP_200_OK)
async def pay_order(
    order_uuid: UUID,
    current_user: User = Depends(AuthenticationRequired()),
    payment_controller: PaymentController = Depends(Factory.get_payment_controller),
    order_controller: OrderController = Depends(Factory.get_order_controller),
):
    return await payment_controller.pay_order(
        request_user=current_user,
        order_uuid=order_uuid,
        order_controller=order_controller,
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def payment_list(
    current_user: User = Depends(AuthenticationRequired()),
    payment_controller: PaymentController = Depends(Factory.get_payment_controller),
) -> Optional[List[PaymentListOut]]:
    return await payment_controller.retrieve(
        user_id=current_user.id,
        many=True,
        join_fields=["order"],
    )


@router.get("/{payment_uuid}", status_code=status.HTTP_200_OK)
async def payment_detail(
    payment_uuid: UUID,
    current_user: User = Depends(AuthenticationRequired()),
    payment_controller: PaymentController = Depends(Factory.get_payment_controller),
) -> PaymentRetrieveOut:
    return await payment_controller.get_by_uuid(
        user_id=current_user.id,
        uuid=payment_uuid,
        join_fields=["order"],
    )
