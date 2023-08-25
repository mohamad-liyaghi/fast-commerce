from fastapi import status, HTTPException, Depends
from .authentication import AuthenticationRequired
from src.app.controllers import VendorController
from src.app.models import User, Vendor


class VendorRequired:
    """
    Make sure a user has an accepted vendor.
    """

    async def __call__(
        self,
        user: User = Depends(AuthenticationRequired()),
        vendor_controller: VendorController = Depends(VendorController),
    ) -> Vendor:
        # Get the accepted vendor for the user.
        vendor = await vendor_controller.retrieve_accepted_vendor(user=user)

        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have an accepted vendor.",
            )

        return vendor
