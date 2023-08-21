from fastapi import HTTPException, status
from src.core.utils import format_key
from src.core.configs import settings
from src.core.handlers import OtpHandler, PasswordHandler, JWTHandler
from src.core.tasks import send_email
from .user import UserController


class AuthController(UserController):
    """
    This Controller handles user registration, verification, and login.
    """

    async def register(self, data: dict) -> None:
        """
        Create a new user in cache and send a verification email.
        """
        email = data.get('email')

        if await self.retrieve(email=email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists.',
            )

        cache_key = await format_key(
            key=settings.CACHE_USER_KEY,
            email=email
        )

        if await self.repository.get_cache(key=cache_key):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is pending verification.',
            )

        # Create and set verification code
        otp = await OtpHandler.create()
        data.setdefault('otp', str(otp))

        # Set user in cache (For 2 minutes)
        await self.repository.create_cache(
            key=cache_key,
            data=data,
            ttl=60 * 2
        )

        send_email.delay(
            subject='Verify your account',
            to_email=email,
            body={'otp': otp, 'first_name': data.get('first_name')},
            template_name='verification.html',
        )

    async def verify(self, email: str, otp: int) -> None:
        """
        Verify a user using OTP.
        """
        if await self.retrieve(email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is already verified.',
            )

        cache_key = await format_key(
            key=settings.CACHE_USER_KEY,
            email=email
        )
        cached_user = await self.repository.get_cache(key=cache_key)

        if not cached_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found in cache.',
            )

        # Validate OTP
        if not await OtpHandler.validate(otp=otp, user=cached_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid OTP.',
            )

        # Remove OTP from cached data and create user in database
        cached_user.pop('otp')
        await self.create(**cached_user)

    async def login(self, email: str, password: str) -> dict:
        user = await self.retrieve(email=email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Active User not found.',
            )

        if not await PasswordHandler.verify_password(
                password=password,
                hashed_password=user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid credentials.',
            )

        return await JWTHandler.create_access_token(
            data={'user_uuid': str(user.uuid)}
        )
