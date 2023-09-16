from fastapi import Depends, status
from fastapi.routing import APIRouter
from typing import List, Optional
from uuid import UUID
from src.core.factory import Factory
from src.app.enums import VendorStatusEnum
from src.core.dependencies import (
    AuthenticationRequired,
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

router = APIRouter(
    tags=["Vendors"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vendor(
    request: VendorCreateIn,
    current_user=Depends(AuthenticationRequired()),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorCreateOut:
    """Create a new pending vendor request."""
    return await vendor_controller.create(
        request_user=current_user, **request.model_dump()
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_vendor_list(
    current_user=Depends(AuthenticationRequired()),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> Optional[List[VendorListOut]]:
    """List of a user's vendor requests."""
    return await vendor_controller.retrieve(owner_id=current_user.id, many=True)


@router.get("/requests/", status_code=status.HTTP_200_OK)
async def get_vendor_requests(
    __=Depends(AdminRequired()),
    _=Depends(AuthenticationRequired()),
    vendor_controller=Depends(Factory.get_vendor_controller),
    status: VendorStatusEnum = VendorStatusEnum.PENDING,
) -> Optional[List[VendorListOut]]:
    """List of all [pending] vendor requests. (can be filtered by status in args)"""
    return await vendor_controller.retrieve(
        status=status, many=True, join_fields=["owner"]
    )


@router.get("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def get_vendor(
    vendor_uuid: UUID,
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorRetrieveOut:
    """Get a vendor information by uuid."""
    return await vendor_controller.get_by_uuid(
        vendor_uuid, join_fields=["owner", "reviewer"]
    )


@router.put("/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def update_vendor(
    vendor_uuid: UUID,
    request: VendorUpdateIn,
    current_user=Depends(AuthenticationRequired()),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorUpdateOut:
    """Update a vendor information by owner."""
    return await vendor_controller.update_vendor(
        vendor_uuid=vendor_uuid, request_user=current_user, **request.model_dump()
    )


@router.put("/status/{vendor_uuid}", status_code=status.HTTP_200_OK)
async def update_vendor_status(
    vendor_uuid: UUID,
    request: VendorUpdateStatusIn,
    current_user=Depends(AuthenticationRequired()),
    __=Depends(AdminRequired()),
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorUpdateStatusOut:
    """Update a vendor status by admin."""
    return await vendor_controller.update_vendor(
        vendor_uuid=vendor_uuid, request_user=current_user, status=request.status
    )
