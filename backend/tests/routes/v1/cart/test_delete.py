import pytest
from uuid import uuid4
from fastapi import status


@pytest.mark.asyncio
class TestCartItemDeleteRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, cart) -> None:
        self.url = f"v1/cart/{str(list(cart.keys())[0])}"

    @pytest.mark.asyncio
    async def test_delete_unauthenticated(self, client) -> None:
        response = await client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_delete(self, admin_client) -> None:
        response = await admin_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.asyncio
    async def test_delete_not_found(self, admin_client) -> None:
        url = f"v1/cart/{uuid4()}"
        response = await admin_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
