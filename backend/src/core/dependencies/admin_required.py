from fastapi import status, HTTPException, Depends
from .authentication import AuthenticationRequired
from src.app.models import User


class AdminRequired:
    """
    Make sure that user is an admin.
    """

    async def __call__(self, user: User = Depends(AuthenticationRequired())) -> None:
        """Make sure that user is an admin."""
        if not user.is_admin:
            raise HTTPException(
                detail="Admin required", status_code=status.HTTP_403_FORBIDDEN
            )
