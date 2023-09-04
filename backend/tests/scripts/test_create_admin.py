import pytest
from tests.utils.faker import create_fake_credential
from tests.fixtures.db import override_get_db
from scripts.create_admin import create_admin


@pytest.mark.asyncio
async def test_create_admin():
    """
    Test create a new admin
    """
    credential = await create_fake_credential()

    user = await create_admin(
        email=credential["email"],
        first_name=credential["first_name"],
        last_name=credential["last_name"],
        password=credential["password"],
        db=override_get_db,
    )
    assert user.is_admin
