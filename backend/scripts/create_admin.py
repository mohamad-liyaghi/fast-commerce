import asyncio
from src.app.models import User
from src.core.database import get_db
from src.core.handlers import PasswordHandler


async def create_admin(
    email: str,
    first_name: str,
    last_name: str,
    password: str,
    db=get_db,
) -> User:
    """
    Create an admin user.
    """
    # Hash password
    hashed_password = await PasswordHandler.hash_password(password)

    # Create admin
    admin = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        is_admin=True,
    )
    async for session in db():
        session.add(admin)
        await session.commit()
        await session.refresh(admin)

    print("Admin created successfully")
    return admin


def get_admin_inputs():
    email = input("Enter admin email: ")
    first_name = input("Enter admin first name: ")
    last_name = input("Enter admin last name: ")
    password = input("Enter admin password: ")
    return email, first_name, last_name, password


if __name__ == "__main__":
    email, first_name, last_name, password = get_admin_inputs()
    asyncio.run(create_admin(email, first_name, last_name, password))
