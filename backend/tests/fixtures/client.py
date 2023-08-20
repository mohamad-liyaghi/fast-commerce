from httpx import AsyncClient
import pytest_asyncio
from src.main import app


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncClient:
    """
    Create a new FastAPI AsyncClient
    """

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def authorized_client(
        client: AsyncClient,
        user,
        user_controller
) -> AsyncClient:
    """
    Create a new user and login/
    """
    password = '1234'
    await user_controller.update(user, password=password)

    response = await client.post(
        "v1/auth/login",
        json={'email': user.email, 'password': password}
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
