from typing import Optional
from src.app.models import User
from src.app.repositories.base import BaseRepository
from src.core.exceptions import UserAlreadyExistError
from src.core.handlers import PasswordHandler


class UserRepository(BaseRepository):
    """
    User repository responsible for user CRUD operations.
    """

    async def create(self, **data):
        """
        Create a user, hashing their password before storing it in the database.
        """
        email = data.get("email")

        if await self.get_by_email(email):
            raise UserAlreadyExistError

        # Hash the user's password
        hashed_password = await PasswordHandler.hash_password(data.pop("password"))
        data.setdefault("password", hashed_password)

        return await super().create(**data)

    async def update(self, instance, **data):
        """
        Update user information, including password hashing if changed.
        """
        password = data.get("password")

        # Hash the password if it has changed
        if password and password != instance.password:
            hashed_password = await PasswordHandler.hash_password(password)
            data["password"] = hashed_password

        return await super().update(instance, **data)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.
        """
        return await self.retrieve(email=email)
