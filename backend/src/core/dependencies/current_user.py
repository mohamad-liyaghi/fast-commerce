from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.app.controllers import UserController
from src.core.factory import Factory
from src.app.models import User


async def get_current_user(
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        user_controller: UserController = Depends(Factory().get_user_controller)
) -> User:
    """
    Return current user if token is valid.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No authentication credentials provided."
        )

    if token.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication scheme."
        )

    user = await user_controller.get_by_uuid(request.user.uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token."
        )

    return user
