from fastapi import status
from uuid import uuid4
import pytest
from src.app.enums import OrderStatusEnum


class TestUpdateToDeliveringRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, paid_order) -> None:
        self.url = f"v1/order/{paid_order.uuid}"
        self.order = paid_order
        self.data = {
            "status": str(OrderStatusEnum.DELIVERING.value),
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_admin(self, admin_client) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_by_user(self, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_already_delivering(self, admin_client, delivering_order):
        url = f"v1/order/{delivering_order.uuid}"
        response = await admin_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_update_invalid_status(self, admin_client):
        self.data["status"] = str(OrderStatusEnum.PENDING_PAYMENT.value)
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_update_not_found(self, admin_client):
        url = f"v1/order/{uuid4()}"
        response = await admin_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
