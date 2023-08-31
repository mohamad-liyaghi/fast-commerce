from fastapi import status
from uuid import uuid4
import pytest


class TestUpdateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, cart) -> None:
        self.url = f"v1/cart/{cart.get('product_uuid')}"
        self.data = {"quantity": 4}

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update(self, admin_client, admin) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_not_cart(self, authorized_client, user) -> None:
        url = f"v1/cart/{uuid4()}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
