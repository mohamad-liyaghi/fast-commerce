from fastapi import HTTPException, status
from src.core.handlers import OtpHandler, PasswordHandler, JWTHandler
from src.core.email import send_email
from .user import UserController


class AuthController(UserController):
    """
    This Controller handles user registration and verification.
    """

    async def register(self, data: dict) -> None:
        """
        Create a new user in cache.
        :param data: the user data
        """
        email = data.get('email')

        # Raise error if user exists in database
        if await self.retrieve(email=email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exists.',
            )

        # Raise error if user exists in cache (Pending verification)
        if await self.repository.get_cache(key=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is pending verification.',
            )

        # Create and set verification code
        otp = await OtpHandler.create()
        data.setdefault('otp', str(otp))

        # Set user in cache (For 2 minutes)
        await self.repository.create_cache(
            key=email,
            data=data,
            ttl=60 * 2
        )

        await send_email(
            subject='Verify your account',
            to_email=email,
            body={'otp': otp, 'first_name': data.get('first_name')},
            template_name='verification.html',
        )

    async def verify(self, email: str, otp: int) -> None:
        """
        Verify a user.
        :param email: the user email
        :param otp: the user otp
        """

        # Raise error if user is already verified
        if await self.retrieve(email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User is already verified.',
            )

        cached_user = await self.repository.get_cache(key=email)
        # Raise error if user is not in cache
        if not cached_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found.',
            )

        # Validate its otp
        validate_opt = await OtpHandler.validate(otp=otp, user=cached_user)

        # Raise error if otp is invalid
        if not validate_opt:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Invalid OTP.',
            )

        # Remove otp from dict and create user in database
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
