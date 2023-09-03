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


class AuthRepository(UserRepository):
    """
    Auth repository is based on the user repository and is responsible for handling
    User creation in cache and verification.
    """

    async def register(self, data: dict) -> dict:
        email = data.get("email")

        # Raise error if user already exists in database.
        if await self.retrieve(email=email):
            raise UserAlreadyExistError

        cache_key = await format_key(key=settings.CACHE_USER_KEY, email=email)

        if await self.get_cache(key=cache_key):
            raise UserPendingVerificationError

        copied_data = data.copy()

        otp = await OtpHandler.create()
        data.setdefault("otp", str(otp))

        # Create user in cache.
        await self.create_cache(key=cache_key, data=data, ttl=settings.CACHE_USER_TTL)
        # Send verification email.
        await self._send_verification_email(
            to_email=email, data={"otp": otp, "first_name": data.get("first_name")}
        )
        return copied_data

    async def verify(self, email: str, otp: int) -> None:
        """
        Verify a user using OTP.
        """
        # Raise error if user already exists in database.
        if await self.retrieve(email=email):
            raise UserAlreadyExistError

        cache_key = await format_key(key=settings.CACHE_USER_KEY, email=email)
        cached_user = await self.get_cache(key=cache_key)

        # IF user is not found in cache, it means user was deleted due to
        # expiration of the TTL.
        if not cached_user:
            raise UserNotFoundError

        # If verification code is invalid, raise an error.
        if not await OtpHandler.validate(otp=otp, user=cached_user):
            raise InvalidVerificationCodeError

        # Remove OTP from cached data and create user in database
        cached_user.pop("otp")
        await self.create(**cached_user)

    async def login(self, email: str, password: str) -> dict:
        user = await self.retrieve(email=email)

        if not user:
            raise UserNotFoundError

        if not await PasswordHandler.verify_password(
            password=password, hashed_password=user.password
        ):
            raise InvalidCredentialsError

        return await JWTHandler.create_access_token(data={"user_uuid": str(user.uuid)})

    @staticmethod
    async def _send_verification_email(to_email: str, data: dict) -> None:
        """Send verification code to user email."""
        send_email.delay(
            subject="Verify your account",
            to_email=to_email,
            body=data,
            template_name="verification.html",
        )
