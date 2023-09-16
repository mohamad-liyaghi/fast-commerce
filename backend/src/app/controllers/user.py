from uuid import UUID
from src.app.controllers.base import BaseController
from src.app.models import User


class UserController(BaseController):
    """
    User controller is responsible for handling user CRUD operations.
    """

    async def update_user(self, uuid: UUID, requesting_user: User, **kwargs) -> User:
        user = await self.get_by_uuid(uuid, id=requesting_user.id)
        return await super().update(user, **kwargs)
