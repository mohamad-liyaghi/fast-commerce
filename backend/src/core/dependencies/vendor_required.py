from fastapi import status, HTTPException, Depends
from .authentication import AuthenticationRequired
from src.app.models import User, Vendor


class VendorRequired:
    """
    Make sure a user has an accepted vendor.
    """

    async def __call__(self, user: User = Depends(AuthenticationRequired())) -> Vendor:
        # Get the accepted vendor for the user.
        vendor = await user.get_accepted_vendor()

        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have an accepted vendor.",
            )

        return vendor
