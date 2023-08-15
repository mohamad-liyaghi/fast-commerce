from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.core.database import Base, get_db
from src.main import app


TEST_DATABASE_URL = settings.TEST_POSTGRES_URL

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db() -> TestingSessionLocal:
    """
    Return a TestingSessionLocal instance
    :return: TestingSessionLocal
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the get_db function
app.dependency_overrides[get_db] = override_get_db
