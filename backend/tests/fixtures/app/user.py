import pytest_asyncio
from faker import Faker
from src.app.models import User
from src.app.controllers import UserController
from src.app.repositories import UserRepository
from tests.utils import create_fake_credential

faker = Faker()


@pytest_asyncio.fixture
async def user_controller(get_test_db, get_test_redis):
    """
    Returns a UserController instance
    """
    return UserController(
        repository=UserRepository(
            model=User,
            database=get_test_db,
            redis=get_test_redis
        )
    )


@pytest_asyncio.fixture
async def user(user_controller):
    """
    Returns a User instance
    """
    return await user_controller.create(**create_fake_credential())


@pytest_asyncio.fixture
async def cached_user(user_controller, client):
    credential = create_fake_credential()
    data = {
            "email": credential['email'],
            "first_name": credential['first_name'],
            "last_name": credential['last_name'],
            "password": credential['password'],
    }
    await client.post("v1/auth/register", json=data)
    return data


@pytest_asyncio.fixture
async def admin(user_controller):
    """
    Returns a User instance
    """
    return await user_controller.create(
        **create_fake_credential(),
        is_admin=True
    )
