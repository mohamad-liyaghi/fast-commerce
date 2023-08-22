from fastapi import HTTPException, status
from src.app.controllers.base import BaseController
from src.app.models import User, VendorStatusEnum
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
        ten_days_ago = datetime.utcnow() - timedelta(days=10)

        if existing_vendor:
            if existing_vendor.status == VendorStatusEnum.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have a pending vendor registration request.",
                )
            elif existing_vendor.status == VendorStatusEnum.ACCEPTED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already have a vendor registered.",
                )
            elif (
                existing_vendor.status == VendorStatusEnum.REJECTED
                and existing_vendor.reviewed_at > ten_days_ago
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
