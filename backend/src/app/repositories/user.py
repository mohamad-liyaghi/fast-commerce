from src.app.repositories.base import BaseRepository
from src.core.exceptions import UserAlreadyExistError
from src.core.handlers import PasswordHandler


class UserRepository(BaseRepository):
    """
    User repository is responsible for handling user CRUD operations.
    """

    async def create(self, **data):
        """
        Create a new user in the database based on the given data.
        """

        if await self.retrieve(email=data.get("email")):
            raise UserAlreadyExistError

        # Hash password
        hashed_password = await PasswordHandler.hash_password(data.pop("password"))
        data.setdefault("password", hashed_password)

        return await super().create(**data)

    async def update(self, instance, **data):
        """
        Update a user from database also hash its password if it was changed.
        """
        password = data.get("password")

        if password and not password == instance.password:
            hashed_password = await PasswordHandler.hash_password(password)
            data["password"] = hashed_password

        return await super().update(instance, **data)
