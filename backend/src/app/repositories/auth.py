from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import (
    UserAlreadyExistError,
    UserPendingVerificationError,
    UserNotFoundError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
)
from src.core.handlers import OtpHandler, PasswordHandler, JWTHandler
from src.core.tasks import send_email
from src.core.configs import settings
from src.core.utils import format_key
from .user import UserRepository
from src.app.models import User


class AuthRepository(UserRepository):
    """
    Auth repository is based on the user repository and is responsible for handling
    User creation in cache and verification.
    """

    def __init__(
        self, model: User, database_session: AsyncSession, redis_session: Redis
    ):
        super().__init__(model, database_session, redis_session)

    async def register_user(self, data: dict) -> dict:
        email = data.get("email")

        user = await self.get_by_email(email=email)
        if user:
            raise UserAlreadyExistError

        cached_user = await self._get_cache_user_by_email(email=email)
        if cached_user:
            raise UserPendingVerificationError

        # Create otp and add it to data.
        data = await self._create_otp(data=data)
        await self._create_cached_user(data=data)
        await self._send_verification_email(
            to_email=email,
            data={"otp": data.get("otp"), "first_name": data.get("first_name")},
        )
        return data

    async def verify_user(self, email: str, otp: int) -> None:
        user = await self.get_by_email(email=email)
        if user:
            raise UserAlreadyExistError

        cached_user = await self._get_cache_user_by_email(email=email)
        if not cached_user:
            raise UserNotFoundError

        verify_otp = await self._verify_otp(otp=otp, cached_user=cached_user)
        if not verify_otp:
            raise InvalidVerificationCodeError

        # If otp is valid, remove it from cached user and create user in database.
        cached_user.pop("otp")
        await self.create(**cached_user)

    async def login_user(self, email: str, password: str) -> dict:
        user = await self.get_by_email(email=email)
        if not user:
            raise UserNotFoundError

        verify_password = await self._verify_password(
            password=password, hashed_password=user.password
        )
        if not verify_password:
            raise InvalidCredentialsError

        return await self._create_access_token(data={"user_uuid": str(user.uuid)})

    async def _get_cache_user_by_email(self, email: str) -> dict:
        key = await self._create_cache_key(email=email)
        return await self.get_cache(key=key)

    async def _create_cached_user(self, data: dict) -> None:
        key = await self._create_cache_key(email=data.get("email"))
        await self.create_cache(key=key, data=data, ttl=settings.CACHE_USER_TTL)

    @staticmethod
    async def _create_cache_key(email: str) -> str:
        return await format_key(key=settings.CACHE_USER_KEY, email=email)

    @staticmethod
    async def _create_otp(data: dict) -> dict:
        otp = await OtpHandler.create()
        data.setdefault("otp", str(otp))
        return data

    @staticmethod
    async def _verify_otp(otp: int, cached_user: dict) -> bool:
        return await OtpHandler.validate(otp=otp, user=cached_user)

    @staticmethod
    async def _verify_password(password: str, hashed_password: str) -> bool:
        return await PasswordHandler.verify_password(
            password=password, hashed_password=hashed_password
        )

    @staticmethod
    async def _create_access_token(data: dict) -> dict:
        return await JWTHandler.create_access_token(data=data)

    @staticmethod
    async def _send_verification_email(to_email: str, data: dict) -> None:
        """Send verification code to user email."""
        send_email.delay(
            subject="Verify your account",
            to_email=to_email,
            body=data,
            template_name="verification.html",
        )
