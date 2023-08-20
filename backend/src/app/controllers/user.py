from fastapi import HTTPException, status
from src.core.controller import BaseController
from uuid import UUID


class UserController(BaseController):
    """
    User controller is responsible for handling user CRUD operations.
    """
    async def retrieve_profile(self, user_uuid: UUID):
        """
        Retrieve a profile by its uuid.
        """
        user = await self.retrieve(uuid=user_uuid)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='user not found.'
            )

        return user
