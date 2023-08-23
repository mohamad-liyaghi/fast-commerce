from fastapi import status, HTTPException, Depends
from src.app.models import User
from .current_user import get_current_user


class AdminRequired:
    """
    Make sure that user is an admin.
    """

    def __init__(self, user: User = Depends(get_current_user)) -> None:
        if not user.is_admin:
            raise HTTPException(
                detail="Admin required", status_code=status.HTTP_403_FORBIDDEN
            )
