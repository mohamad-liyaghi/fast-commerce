import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import Base
from tests.mocks import override_get_db, engine


@pytest_asyncio.fixture(scope="function")
async def get_test_db() -> AsyncSession:
    """
    Reset database and return a session
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in override_get_db():
        yield session
