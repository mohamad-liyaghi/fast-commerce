from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.app.controllers import UserController
from src.core.dependencies import AuthenticationRequired
from src.app.schemas.in_ import UserIn
from src.app.schemas.out import UserOut
from src.app.models import User

router = APIRouter(
    tags=["Users"],
)


@router.get("/{user_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_user(
    user_uuid: UUID,
    _: User = Depends(AuthenticationRequired()),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserOut:
    """Retrieve a user's information by its uuid."""
    return await user_controller.get_by_uuid(uuid=user_uuid)


@router.put("/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_user(
    request: UserIn,
    user_uuid: UUID,
    user_controller: User = Depends(Factory().get_user_controller),
    current_user: AuthenticationRequired = Depends(AuthenticationRequired()),
) -> UserOut:
    """Update a user's information by its owner."""
    return await user_controller.update_user(
        uuid=user_uuid, requesting_user=current_user, **request.model_dump()
    )
