from fastapi import status
from uuid import uuid4
import pytest
from src.app.enums import OrderStatusEnum


class TestUpdateToDeliveredgRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, delivering_order) -> None:
        self.url = f"v1/order/{delivering_order.uuid}"
        self.order = delivering_order
        self.data = {
            "status": str(OrderStatusEnum.DELIVERED.value),
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_owner(self, admin_client, admin) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert admin.id == self.order.user_id

    @pytest.mark.asyncio
    async def test_update_by_other_user(self, authorized_client, user) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert user.id != self.order.user_id

    @pytest.mark.asyncio
    async def test_update_already_delivered(self, admin_client, delivered_order):
        url = f"v1/order/{delivered_order.uuid}"
        response = await admin_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert delivered_order.status == OrderStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_update_invalid_status(self, admin_client):
        self.data["status"] = str(OrderStatusEnum.PENDING_PAYMENT.value)
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_update_not_found(self, authorized_client):
        url = f"v1/order/{uuid4()}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
