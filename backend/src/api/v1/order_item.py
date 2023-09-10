from fastapi.routing import APIRouter
from fastapi import Depends, status
from typing import List, Optional
from src.core.dependencies import AuthenticationRequired, VendorRequired, AdminRequired
from src.app.controllers import OrderItemController, OrderController
from src.core.factory import Factory
from src.app.schemas.out import OrderItemList
from src.app.enums import OrderItemStatusEnum
from src.app.models import Vendor

router = APIRouter(
    tags=["Order Items"],
)


@router.get("/preparing", status_code=status.HTTP_200_OK)
async def get_preparing_order_items(
    _: AuthenticationRequired = Depends(),
    vendor: Vendor = Depends(VendorRequired()),
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


@router.get("/delivering", status_code=status.HTTP_200_OK)
async def get_delivering_order_items(
    _: AuthenticationRequired = Depends(),
    __: AdminRequired = Depends(AdminRequired()),
    order_item_controller: OrderItemController = Depends(
        Factory.get_order_item_controller
    ),
) -> Optional[List[OrderItemList]]:
    """
    Return list of prepared objects that are delivering to the system's center
    """
    return await order_item_controller.retrieve(
        status=OrderItemStatusEnum.DELIVERING, many=True, join_fields=["product"]
    )
