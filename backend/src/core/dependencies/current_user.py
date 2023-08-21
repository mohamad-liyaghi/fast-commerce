from fastapi import Depends, Request, HTTPException, status
from src.app.controllers import UserController
from src.core.factory import Factory
from src.app.models import User


async def get_current_user(
    request: Request,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> User:
    """
    Return current user if token is valid.
    """
    user = await user_controller.get_by_uuid(request.user.uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token."
        )

    return user
