from fastapi import HTTPException, status
from src.app.controllers.base import BaseController
from src.app.models import User
from src.core.sql.types import UUIDType


class UserController(BaseController):
    """
    User controller is responsible for handling user CRUD operations.
    """

    async def update(self, uuid: UUIDType, requesting_user: User, **kwargs) -> User:
        """
        Update the user's profile if they have permission.
        """
        user = await self.get_by_uuid(uuid)

        if user != requesting_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this profile.",
            )

        return await super().update(user, **kwargs)
