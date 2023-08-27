from fastapi import Depends, status, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.app.models import User
from src.core.factory import Factory
from src.app.controllers import UserController


class AuthenticationRequired:
    """
    Make sure the user is authenticated.
    """

    async def __call__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        user_controller: UserController = Depends(Factory().get_user_controller),
    ) -> User:
        """
        Check if user is authenticated and return the user.
        """
        if not token:
            raise HTTPException(
                detail="Authentication required", status_code=status.HTTP_403_FORBIDDEN
            )
        return await user_controller.get_by_uuid(
            request.user.uuid, not_found_message="User not found"
        )
