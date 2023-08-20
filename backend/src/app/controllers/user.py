from fastapi import HTTPException, status
from src.core.controller import BaseController
from src.app.models import User
from uuid import UUID


class UserController(BaseController):
    """
    User controller is responsible for handling user CRUD operations.
    """

    async def get_by_uuid(self, uuid: UUID):
        user = await super().get_by_uuid(uuid)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found.'
            )

        return user

    async def update_user(
            self,
            uuid: UUID,
            requesting_user: User,
            **kwargs
    ) -> User:
        """
        Update the user's profile if they have permission.
        """
        user = await self.get_by_uuid(uuid)

        if user != requesting_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this profile."
            )

        return await super().update(user, **kwargs)

