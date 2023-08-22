from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.core.dependencies import AuthenticationRequired, get_current_user
from src.app.schemas import VendorCreateIn, VendorCreateOut, VendorRetrieveOut

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


@router.get("/{vendor_uuid}")
async def get_vendor(
    vendor_uuid: UUID,
    vendor_controller=Depends(Factory.get_vendor_controller),
) -> VendorRetrieveOut:
    """Get a vendor."""
    return await vendor_controller.get_by_uuid(vendor_uuid)
