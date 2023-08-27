from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.core.configs import settings
from src.core.database import get_db
from src.main import app

engine = create_async_engine(settings.TEST_POSTGRES_URL)


async def get_test_db():
    """
    Return a TestingSessionLocal instance
    :return: TestingSessionLocal
    """
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


# Override the get_db function
app.dependency_overrides[get_db] = get_test_db
