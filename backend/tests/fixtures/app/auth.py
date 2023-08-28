import pytest_asyncio
from src.app.models import User
from src.app.controllers import AuthController
from src.app.repositories import UserRepository


@pytest_asyncio.fixture
async def auth_controller(get_test_db, get_test_redis):
    """
    Returns a AuthController instance
    """
    return AuthController(
        repository=UserRepository(
            model=User, database=get_test_db, redis=get_test_redis
        )
    )
