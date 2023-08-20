from fastapi import Depends, status
from fastapi.routing import APIRouter
from src.core.dependencies import get_current_user
from src.app.schemas import ProfileOut


profile_router = APIRouter(
    tags=['Profiles'],
)


@profile_router.get('/me', status_code=status.HTTP_200_OK)
async def retrieve_profile(
        current_user=Depends(get_current_user),
) -> ProfileOut:
    """Get profile of the current user."""
    return current_user
