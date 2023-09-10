from fastapi.routing import APIRouter
from fastapi import Depends, status
from typing import List, Optional
from src.core.dependencies import AuthenticationRequired, VendorRequired
from src.app.controllers import OrderItemController, OrderController
from src.core.factory import Factory
from src.app.schemas.out import OrderItemList

router = APIRouter(
    tags=["Order Items"],
)


@router.get("/preparing", status_code=status.HTTP_200_OK)
async def get_preparing_order_items_(
    _: AuthenticationRequired = Depends(),
    vendor: VendorRequired = Depends(VendorRequired()),
    order_item_controller: OrderItemController = Depends(
        Factory.get_order_item_controller
    ),
    order_controller: OrderController = Depends(Factory.get_order_controller),
) -> Optional[List[OrderItemList]]:
    """
    Return list of preparing order items for a vendor
    """
    return await order_item_controller.get_preparing(
        vendor=vendor, order_controller=order_controller
    )
