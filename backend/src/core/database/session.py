from sqlalchemy.orm import Session
from .base import SessionLocal


def get_db() -> Session:
    """
    Get database session
    :return: database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
