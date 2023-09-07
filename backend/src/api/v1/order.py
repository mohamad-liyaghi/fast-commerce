from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from src.core.dependencies import AuthenticationRequired, CartRequired
from src.app.controllers import (
    OrderController,
    OrderItemController,
    CartController,
    ProductController,
)
from src.core.factory import Factory
from src.app.schemas.in_ import OrderCreateIn


router = APIRouter(
    tags=["Order"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: OrderCreateIn,
    request_user: AuthenticationRequired = Depends(AuthenticationRequired()),
    cart: CartRequired = Depends(CartRequired()),
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
