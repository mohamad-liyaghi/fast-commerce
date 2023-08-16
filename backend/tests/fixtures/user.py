import pytest_asyncio
from faker import Faker
from src.app.models import User
from src.app.controllers import UserController
from src.app.repositories import UserRepository
from tests.utils import create_fake_credential

faker = Faker()


@pytest_asyncio.fixture
async def user_controller(get_test_db):
    """
    Returns a UserController instance
    """
    return UserController(
        repository=UserRepository(model=User, database=get_test_db)
    )


@pytest_asyncio.fixture
async def user(user_controller):
    """
    Returns a User instance
    """
    return await user_controller.create(**create_fake_credential())


@pytest_asyncio.fixture
async def admin(user_controller):
    """
    Returns a User instance
    """
    return await user_controller.create(
        **create_fake_credential(),
        is_admin=True
    )
