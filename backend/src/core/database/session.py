from sqlalchemy.ext.asyncio import AsyncSession
from .base import async_session


async def get_db() -> AsyncSession:
    """Return a database session."""
    async with async_session() as session:
        yield session
