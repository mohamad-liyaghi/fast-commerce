from httpx import AsyncClient
import pytest_asyncio
from src.main import app
from src.core.handlers import JWTHandler


@pytest_asyncio.fixture(scope="class")
async def client() -> AsyncClient:
    """
    Create a new FastAPI AsyncClient
    """

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="class")
async def authorized_client(user, client) -> AsyncClient:
    """
    Create a new user and login
    """
    access_token = await JWTHandler.create_access_token(
        data={"user_uuid": str(user.uuid)}
    )
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest_asyncio.fixture(scope="class")
async def admin_client(admin, client) -> AsyncClient:
    """
    Create a new admin and login
    """
    access_token = await JWTHandler.create_access_token(
        data={"user_uuid": str(admin.uuid)}
    )
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
