from fastapi import Depends, status
from fastapi.routing import APIRouter
from uuid import UUID
from src.core.factory import Factory
from src.app.controllers import UserController
from src.core.dependencies import AuthenticationRequired
from src.app.schemas import ProfileOut


profile_router = APIRouter(
    tags=['Profiles'],
)


@profile_router.get('/{user_uuid}', status_code=status.HTTP_200_OK)
async def retrieve_profile(
    user_uuid: UUID,
    user_controller: UserController = Depends(
        Factory().get_user_controller
    ),
    _: AuthenticationRequired = Depends(AuthenticationRequired)
) -> ProfileOut:
    """Retrieve a profile by its uuid."""
    return await user_controller.retrieve_profile(user_uuid=user_uuid)
