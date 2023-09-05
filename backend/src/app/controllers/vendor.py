from fastapi import HTTPException, status
from uuid import UUID
from src.app.controllers.base import BaseController
from src.app.models import User, Vendor
from src.app.enums import VendorStatusEnum
from src.core.exceptions import (
    AcceptedVendorExistsException,
    PendingVendorExistsException,
    RejectedVendorExistsException,
    UpdateVendorDenied,
    UpdateVendorStatusDenied,
)


class VendorController(BaseController):
    """
    Controller for managing vendor registration and requests.
    """

    async def create(self, request_user: User, **vendor_data) -> Vendor:
        """
        Create a new vendor registration for request_user.
        Rules:
        - A user can only have one pending vendor registration request.
        - A user can only have one accepted vendor registration.
        - A user can only have one rejected vendor registration request
         in the last 10 days.
        """

        try:
            return await super().create(request_user=request_user, **vendor_data)

        except PendingVendorExistsException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a pending vendor registration.",
            )
        except AcceptedVendorExistsException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have an accepted vendor registration.",
            )
        except RejectedVendorExistsException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have a rejected vendor registration in the last 10 days.",
            )

    async def update(self, vendor_uuid: UUID | str, request_user: User, **data) -> Vendor:
        vendor = await self.get_by_uuid(vendor_uuid)
        try:
            return await super().update(
                instance=vendor, request_user=request_user, **data
            )

        except UpdateVendorStatusDenied:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update vendor status.",
            )
        except UpdateVendorDenied:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this vendor.",
            )

    async def retrieve_accepted_vendor(self, user: User):
        """
        Retrieve a vendor and join the owner.
        """
        return await self.retrieve(owner_id=user.id, status=VendorStatusEnum.ACCEPTED)
