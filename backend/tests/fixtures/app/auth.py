import pytest_asyncio
from src.app.models import User
from src.app.controllers import AuthController
from src.app.repositories import AuthRepository


@pytest_asyncio.fixture(scope="class")
async def auth_controller(get_test_db, get_test_redis):
    """
    Returns a AuthController instance
    """
    return AuthController(
        repository=AuthRepository(
            model=User, database_session=get_test_db, redis_session=get_test_redis
        )
    )
