from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.app.controllers import UserController
from src.core.dependencies import AuthenticationRequired
from src.app.schemas.in_ import ProfileUpdateIn
from src.app.schemas.out import ProfileOut

router = APIRouter(
    tags=["Profiles"],
)


@router.get("/{user_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_profile(
    user_uuid: UUID,
    _: AuthenticationRequired = Depends(AuthenticationRequired()),
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> ProfileOut:
    """Retrieve a profile by its uuid."""
    return await user_controller.get_by_uuid(uuid=user_uuid)


@router.put("/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_profile(
    request: ProfileUpdateIn,
    user_uuid: UUID,
    user_controller: UserController = Depends(Factory().get_user_controller),
    current_user: AuthenticationRequired = Depends(AuthenticationRequired()),
) -> ProfileOut:
    """Update a profile by its owner."""
    return await user_controller.update(
        uuid=user_uuid, requesting_user=current_user, **request.model_dump()
    )
