from fastapi import status
import pytest


class TestCreateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = "v1/order/"
        self.data = {"delivery_address": "ir"}

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_empty_cart(self, authorized_client):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create(self, admin_client, cart):
        response = await admin_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
