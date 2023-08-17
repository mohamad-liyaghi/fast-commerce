from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.factory import Factory
from src.app.schemas import UserRegisterIn
from src.app.controllers import AuthController


auth_router = APIRouter(
    tags=['Auth'],
)


@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
        request: UserRegisterIn,
        auth_controller: AuthController = Depends(
            Factory().get_auth_controller
        ),
) -> dict:
    """Register a new user."""
    await auth_controller.register(data=request.dict())
    return {'success': 'user and is pending verification.'}
