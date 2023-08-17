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
