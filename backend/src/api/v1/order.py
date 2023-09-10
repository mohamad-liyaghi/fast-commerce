from fastapi.routing import APIRouter
from fastapi import Depends, status
from typing import List, Optional
from uuid import UUID
from src.core.dependencies import AuthenticationRequired, CartRequired
from src.app.controllers import (
    OrderController,
    OrderItemController,
    CartController,
    ProductController,
)
from src.core.factory import Factory
from src.app.schemas.in_ import OrderCreateIn
from src.app.schemas.out import OrderListOut, OrderRetrieveOut
from src.app.models import User


router = APIRouter(
    tags=["Order"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: OrderCreateIn,
    request_user: User = Depends(AuthenticationRequired()),
    cart: dict = Depends(CartRequired()),
    order_controller: OrderController = Depends(Factory.get_order_controller),
    order_item_controller: OrderItemController = Depends(
        Factory.get_order_item_controller
    ),
    product_controller: ProductController = Depends(Factory.get_product_controller),
    cart_controller: CartController = Depends(Factory.get_cart_controller),
) -> dict:
    await order_controller.create_order(
        request_user=request_user,
        order_item_controller=order_item_controller,
        cart_controller=cart_controller,
        product_controller=product_controller,
        cart=cart,
        **request.model_dump(),
    )
    return {"ok": "created"}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(
    request_user: User = Depends(AuthenticationRequired()),
    order_controller: OrderController = Depends(Factory.get_order_controller),
) -> Optional[List[OrderListOut]]:
    return await order_controller.retrieve(
        user_id=request_user.id,
        many=True,
        order_by=["created_at"],
        descending=True,
        limit=40,
        join_fields=["order_items"],
    )


@router.get("/{order_uuid}", status_code=status.HTTP_200_OK)
async def get_order(
    order_uuid: UUID,
    request_user: User = Depends(AuthenticationRequired()),
    order_controller: OrderController = Depends(Factory.get_order_controller),
) -> Optional[OrderRetrieveOut]:
    return await order_controller.get_by_uuid(
        uuid=order_uuid,
        user_id=request_user.id,
        join_fields=["order_items"],
    )
