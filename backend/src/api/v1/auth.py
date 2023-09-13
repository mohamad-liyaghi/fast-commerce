from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.factory import Factory
from src.app.schemas.in_ import UserRegisterIn, UserVerifyIn, UserLoginIn
from src.app.controllers import AuthController


router = APIRouter(
    tags=["Authentication"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: UserRegisterIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Register a new user."""
    return await auth_controller.register_user(data=request.model_dump())


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify(
    request: UserVerifyIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Verify a user by its otp code."""
    await auth_controller.verify_user(email=request.email, otp=request.otp)
    return {"success": "user verified."}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: UserLoginIn,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> dict:
    """Login a user."""
    token = await auth_controller.login_user(
        email=request.email, password=request.password
    )
    return {"access_token": token, "token_type": "bearer"}
