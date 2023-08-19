import pytest
from tests.utils import create_fake_credential
from scripts.create_admin import create_admin

@pytest.mark.asyncio
async def test_create_admin(get_test_db):
    """
    Test create a new admin
    """
    credential = await create_fake_credential()

    user = await create_admin(
        email=credential['email'],
        first_name=credential['first_name'],
        last_name=credential['last_name'],
        password=credential['password'],
        db=get_test_db
    )
    assert user.is_admin
