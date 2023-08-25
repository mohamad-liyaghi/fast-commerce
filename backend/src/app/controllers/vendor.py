from fastapi import HTTPException, status
from uuid import UUID
from sqlalchemy.orm import selectinload
from src.app.controllers.base import BaseController
from src.app.models import User, VendorStatus
from datetime import datetime, timedelta


class VendorController(BaseController):
    """
    Controller for managing vendor registration and requests.
    """

    async def create(self, request_user: User, **vendor_data):
        """
        Create a new vendor registration for request_user.
        Rules:
        - A user can only have one pending vendor registration request.
        - A user can only have one accepted vendor registration.
        - A user can only have one rejected vendor registration request in the last 10 days.
        """

        # Check if the user has a pending, accepted, or recently rejected vendor request
        existing_vendor = await self.retrieve(owner_id=request_user.id, last=True)

        if existing_vendor:
            if existing_vendor.status == VendorStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have a pending vendor registration request.",
                )
            elif existing_vendor.status == VendorStatus.ACCEPTED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have a vendor registered.",
                )
            elif (
                existing_vendor.status == VendorStatus.REJECTED
                and existing_vendor.reviewed_at > datetime.utcnow() - timedelta(days=10)
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="""
                    Your previous vendor registration request was rejected.
                    Please try again after 10 days.
                    """,
                )

        # Create a new vendor and return it
        return await super().create(owner_id=request_user.id, **vendor_data)

    async def update(self, vendor_uuid: UUID, request_user: User, **data):
        vendor = await self.get_by_uuid(vendor_uuid)

        if data.get("status") and not request_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Admins can update vendor status.",
            )

        if not data.get("status") and not request_user.id == vendor.owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot update others vendor record.",
            )

        return await super().update(vendor, **data)

    async def retrieve_accepted_vendor(self, user: User):
        """
        Retrieve a vendor and join the owner.
        """
        return await self.retrieve(owner_id=user.id, status=VendorStatus.ACCEPTED)
