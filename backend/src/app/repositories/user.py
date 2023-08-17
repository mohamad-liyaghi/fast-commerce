from src.core.handlers import PasswordHandler
from src.core.repository import BaseRepository


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

    # TODO: Move to a separate repository
    async def create_cache(self, redis, key, data, ttl):
        """
        Create a new user in cache. (with its verification code)
        """
        # Set in cache
        await redis.hset(key, mapping=data)
        # Set TTL
        await redis.expire(key, ttl)

    async def get_cache(self, redis, key):
        """
        Get user from cache.
        """
        result = await redis.hget(key, 'verification_code')
        return result

    async def delete_cache(self, redis, email):
        """
        Delete user from cache.
        """
        await redis.hdel(email)
