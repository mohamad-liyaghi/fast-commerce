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
from src.app.schemas.in_ import (
    VendorCreateIn,
    VendorUpdateStatusIn,
    VendorUpdateIn,
)
from src.app.schemas.out import (
    VendorCreateOut,
    VendorRetrieveOut,
    VendorUpdateStatusOut,
    VendorUpdateOut,
    VendorListOut,
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
    """Create a new pending vendor."""
    return await vendor_controller.create(
        request_user=current_user, **request.model_dump()
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_vendor_list(
    _=Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> Union[VendorListOut, None]:
    """List of a users vendor requests."""
    return await vendor_controller.retrieve(owner_id=current_user.id, many=True)


@router.get("/requests/", status_code=status.HTTP_200_OK)
async def get_vendor_requests(
    _=Depends(AuthenticationRequired),
    __=Depends(AdminRequired),
    vendor_controller=Depends(Factory.get_vendor_controller),
    status: VendorStatus = VendorStatus.PENDING,
) -> Union[VendorListOut, None]:
    """List of all [pending] vendor requests. (can be filtered by status in args)"""
    return await vendor_controller.retrieve(status=status, many=True)


@router.get("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def get_vendor(
    vendor_uuid: UUID,
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorRetrieveOut:
    """Retrieve a vendor if exists."""
    return await vendor_controller.get_by_uuid(vendor_uuid)


@router.put("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def update_vendor(
    vendor_uuid: UUID,
    request: VendorUpdateIn,
    _=Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorUpdateOut:
    """Update a vendor information by owner."""
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
