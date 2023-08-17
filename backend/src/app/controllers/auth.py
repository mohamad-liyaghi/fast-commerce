from fastapi import HTTPException, status
from src.core.handlers import OtpHandler
from .user import UserController


class AuthController(UserController):
    """
    This Controller handles user registration and verification.
    """

    async def register(self, redis, data) -> None:
        """
        Create a new user in cache.
        :param redis: the redis client
        :param data: the user data
        """
        email = data.pop('email')

        # Check if user exists
        user = await self.retrieve(email=email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists.',
            )

        # Check cache if user exists
        redis_user = await self.repository.get_cache(
            redis=redis,
            key=email
        )

        if redis_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is pending verification.',
            )

        # Create and set verification code
        data.setdefault('verification_code', str(OtpHandler.create()))

        # Set user in cache
        await self.repository.create_cache(
            redis=redis,
            key=email,
            data=data,
            ttl=60 * 2
        )

    def verify(self):
        pass

    def login(self):
        pass
