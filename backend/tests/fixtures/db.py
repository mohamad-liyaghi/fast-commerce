import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from tests.shared.db import get_test_db as get_test_db_func, engine
from src.core.database import Base


@pytest_asyncio.fixture
async def get_test_db() -> AsyncSession:
    """
    Reset database and return a session
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_test_db_func():
        yield session
