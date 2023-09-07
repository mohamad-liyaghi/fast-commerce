from fastapi import status
import pytest


class TestOrderListRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = "v1/order/"

    @pytest.mark.asyncio
    async def test_get_unauthorized(self, client):
        response = await client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_get_empty(self, admin_client):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_get(self, admin_client, order):
        response = await admin_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is not None
