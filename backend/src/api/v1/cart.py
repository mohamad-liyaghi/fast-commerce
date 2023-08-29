from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired
from src.app.controllers import CartController, ProductController
from src.app.schemas.in_ import CartAddIn


router = APIRouter(
    tags=["Cart"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_cart_item(
    request: CartAddIn,
    current_user=Depends(AuthenticationRequired()),
    cart_controller: CartController = Depends(Factory.get_cart_controller),
    product_controller: ProductController = Depends(Factory.get_product_controller),
) -> dict:
    await cart_controller.add_item(
        request_user=current_user,
        product_controller=product_controller,
        **request.model_dump()
    )
    return {"ok": "added"}
