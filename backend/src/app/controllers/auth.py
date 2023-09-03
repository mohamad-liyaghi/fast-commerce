from fastapi import HTTPException, status
from src.core.exceptions import (
    UserAlreadyExistError,
    UserPendingVerificationError,
    UserNotFoundError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
)
from .user import UserController


class AuthController(UserController):
    """
    This Controller handles user registration, verification, and login.
    """

    async def register(self, data: dict) -> dict:
        """
        Create a new user in cache and send verification email.
        """
        try:
            return await self.repository.register(data=data)
        except UserAlreadyExistError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.",
            )
        except UserPendingVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is pending verification.",
            )

    async def verify(self, email: str, otp: int) -> None:
        """
        Verify a user using OTP.
        """
        try:
            await self.repository.verify(email=email, otp=otp)
        except UserAlreadyExistError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already authenticated.",
            )
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        except InvalidVerificationCodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid verification code.",
            )

    async def login(self, email: str, password: str) -> dict:
        try:
            return await self.repository.login(email=email, password=password)
        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        except InvalidCredentialsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials.",
            )
