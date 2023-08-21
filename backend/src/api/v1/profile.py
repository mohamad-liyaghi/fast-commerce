from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.app.controllers import UserController
from src.core.dependencies import AuthenticationRequired, get_current_user
from src.app.schemas import ProfileOut, ProfileUpdateIn

profile_router = APIRouter(
    tags=["Profiles"],
)


@profile_router.get("/{user_uuid}", status_code=status.HTTP_200_OK)
async def retrieve_profile(
    user_uuid: UUID,
    user_controller: UserController = Depends(Factory().get_user_controller),
    _: AuthenticationRequired = Depends(AuthenticationRequired),
) -> ProfileOut:
    """Retrieve a profile by its uuid."""
    return await user_controller.get_by_uuid(uuid=user_uuid)


@profile_router.put("/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_profile(
    request: ProfileUpdateIn,
    user_uuid: UUID,
    user_controller: UserController = Depends(Factory().get_user_controller),
    _: AuthenticationRequired = Depends(AuthenticationRequired),
    current_user=Depends(get_current_user),
) -> ProfileOut:
    """Update a profile by its uuid."""
    return await user_controller.update(
        uuid=user_uuid, requesting_user=current_user, **request.model_dump()
    )
