import pytest_asyncio
from src.app.models import User
from src.app.controllers import UserController
from src.app.repositories import UserRepository
from tests.utils.faker import create_fake_credential


@pytest_asyncio.fixture(scope="session")
async def user_controller(get_test_db, get_test_redis):
    """
    Returns a UserController instance
    """
    return UserController(
        repository=UserRepository(
            model=User, database_session=get_test_db, redis_session=get_test_redis
        )
    )


@pytest_asyncio.fixture(scope="session")
async def user(user_controller):
    """
    Returns a User instance
    """
    credentials = await create_fake_credential()
    return await user_controller.create(**credentials)


@pytest_asyncio.fixture(scope="session")
async def cached_user(user_controller, client):
    credential = await create_fake_credential()
    data = {
        "email": credential["email"],
        "first_name": credential["first_name"],
        "last_name": credential["last_name"],
        "password": credential["password"],
    }
    await client.post("v1/auth/register", json=data)
    return data


@pytest_asyncio.fixture(scope="session")
async def admin(user_controller):
    """
    Returns a User instance
    """
    credential = await create_fake_credential()
    return await user_controller.create(**credential, is_admin=True)
