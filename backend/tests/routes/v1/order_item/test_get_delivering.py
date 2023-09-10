import pytest
from fastapi import status


@pytest.mark.asyncio
class TestRetrieveDeliveringOrderItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/order_item/delivering"

    @pytest.mark.asyncio
    async def test_get_unauthorized(self, client):
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_not_admin(self, authorized_client):
        response = await authorized_client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_empty(self, admin_client):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get_empty_with_preparing(self, admin_client, preparing_order_item):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get(self, admin_client, delivering_order_item):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
