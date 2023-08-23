from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.app.models import VendorStatus
from src.core.dependencies import (
    AuthenticationRequired,
    get_current_user,
    AdminRequired,
)
from src.app.schemas import (
    VendorCreateIn,
    VendorCreateOut,
    VendorRetrieveOut,
    VendorUpdateStatusIn,
    VendorUpdateStatusOut,
    VendorUpdateIn,
    VendorUpdateOut,
)
from typing import List, Union

router = APIRouter(
    tags=["Vendors"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vendor(
    request: VendorCreateIn,
    _=Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorCreateOut:
    """Register for creating a vendor."""
    return await vendor_controller.create(
        request_user=current_user, **request.model_dump()
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_vendor_list(
    _=Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> Union[List[VendorRetrieveOut], None]:
    """Return a users vendor requests list"""
    return await vendor_controller.retrieve(owner_id=current_user.id, many=True)


@router.get("/requests/", status_code=status.HTTP_200_OK)
async def get_vendor_requests(
    _=Depends(AuthenticationRequired),
    __=Depends(AdminRequired),
    vendor_controller=Depends(Factory.get_vendor_controller),
    status: VendorStatus = VendorStatus.PENDING,
) -> Union[List[VendorRetrieveOut], None]:
    """Return a users vendor requests list"""
    return await vendor_controller.retrieve(status=status, many=True)


@router.get("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def get_vendor(
    vendor_uuid: UUID,
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorRetrieveOut:
    """Get a vendor."""
    return await vendor_controller.get_by_uuid(vendor_uuid)


@router.put("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def update_vendor(
    vendor_uuid: UUID,
    request: VendorUpdateIn,
    _=Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorUpdateOut:
    """Update a vendor."""
    vendor = await vendor_controller.get_by_uuid(vendor_uuid)
    return await vendor_controller.update(
        vendor=vendor, request_user=current_user, **request.model_dump()
    )


@router.put("/status/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def update_vendor_status(
    vendor_uuid: UUID,
    request: VendorUpdateStatusIn,
    _=Depends(AuthenticationRequired),
    __=Depends(AdminRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorUpdateStatusOut:
    """Update a vendors status by admin."""
    vendor = await vendor_controller.get_by_uuid(vendor_uuid)
    return await vendor_controller.update(
        vendor=vendor, request_user=current_user, status=request.status
    )
