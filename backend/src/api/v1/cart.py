from fastapi import Depends, status
from fastapi.routing import APIRouter
from typing import List, Optional
from uuid import UUID
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired
from src.app.controllers import CartController, ProductController
from src.app.schemas.in_ import CartAddIn, CartUpdateIn
from src.app.schemas.out import CartListOut


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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_cart_items(
    current_user=Depends(AuthenticationRequired()),
    cart_controller: CartController = Depends(Factory.get_cart_controller),
) -> Optional[List[CartListOut]]:
    return await cart_controller.get_items(request_user=current_user)


@router.put("/{product_uuid}", status_code=status.HTTP_200_OK)
async def update_cart_item(
    product_uuid: UUID | str,
    request: CartUpdateIn,
    current_user=Depends(AuthenticationRequired()),
    cart_controller: CartController = Depends(Factory.get_cart_controller),
) -> dict:
    await cart_controller.update_item(
        request_user=current_user, product_uuid=product_uuid, **request.model_dump()
    )
    return {"ok": "updated"}


@router.delete("/{product_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart_item(
    product_uuid: UUID | str,
    current_user=Depends(AuthenticationRequired()),
    cart_controller: CartController = Depends(Factory.get_cart_controller),
) -> None:
    await cart_controller.delete_item(
        request_user=current_user, product_uuid=product_uuid
    )
