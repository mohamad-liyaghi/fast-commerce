from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.factory import Factory
from src.app.schemas import (
    UserRegisterIn,
    UserVerifyIn,
    UserLoginIn,
)
from src.app.controllers import AuthController


router = APIRouter(
    tags=["Auth"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Register a new user."""
    await auth_controller.register(data=request.model_dump())
    return {"success": "user and is pending verification."}


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify(
    request: UserVerifyIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Verify a user by its otp code."""
    await auth_controller.verify(email=request.email, otp=request.otp)
    return {"success": "user verified."}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: UserLoginIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Login a user."""
    token = await auth_controller.login(email=request.email, password=request.password)
    return {"access_token": token, "token_type": "bearer"}
