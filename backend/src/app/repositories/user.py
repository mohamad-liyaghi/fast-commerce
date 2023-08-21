from src.core.handlers import PasswordHandler
from src.app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """
    User repository is responsible for handling user CRUD operations.
    """

    async def create(self, **data):
        # Hash password before creating user
        hashed_password = await PasswordHandler.hash_password(
            data.pop('password')
        )
        data.setdefault('password', hashed_password)
        return await super().create(**data)

    async def update(self, instance, **data):
        password = data.get('password')

        if password and not password == instance.password:
            hashed_password = await PasswordHandler.hash_password(
                password
            )
            data['password'] = hashed_password

        return await super().update(instance, **data)
