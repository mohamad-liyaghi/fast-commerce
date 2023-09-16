from fastapi import HTTPException, status
from src.core.exceptions import (
    UserAlreadyExistError,
    UserPendingVerificationError,
    UserNotFoundError,
    InvalidVerificationCodeError,
    InvalidCredentialsError,
)
from .user import UserController
from src.app.repositories import AuthRepository


class AuthController(UserController):
    """
    This Controller handles user registration, verification, and login.
    """

    def __init__(self, repository: AuthRepository):
        self.repository = repository
        super().__init__(repository)

    async def register_user(self, data: dict) -> dict:
        """
        Create a new user in cache and send verification email.
        """
        try:
            return await self.repository.register_user(data=data)

        except UserAlreadyExistError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )

        except UserPendingVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User exists and is pending verification.",
            )

    async def verify_user(self, email: str, otp: int) -> None:
        try:
            await self.repository.verify_user(email=email, otp=otp)

        except UserAlreadyExistError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already verified",
            )

        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )

        except InvalidVerificationCodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid verification code.",
            )

    async def login_user(self, email: str, password: str) -> dict:
        try:
            return await self.repository.login_user(email=email, password=password)

        except UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist",
            )

        except InvalidCredentialsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Password does not match",
            )
