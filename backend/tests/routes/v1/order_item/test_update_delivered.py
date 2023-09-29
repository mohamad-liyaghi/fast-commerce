from fastapi import status
from uuid import uuid4
import pytest
from src.app.enums import OrderItemStatusEnum


class TestUpdateDeliveredItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, delivering_order_item) -> None:
        self.url = f"v1/order_item/status/{delivering_order_item.uuid}"
        self.order_item = delivering_order_item
        self.data = {
            "status": str(OrderItemStatusEnum.DELIVERED.value),
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized_fails(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_delivered_item_fails(
        self, admin_client, delivered_order_item
    ):
        url = f"v1/order_item/status/{delivered_order_item.uuid}"
        response = await admin_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert delivered_order_item.status == OrderItemStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_update_by_admin(self, admin_client) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_by_non_admin_fails(self, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_with_invalid_status_fails(self, authorized_client):
        self.data["status"] = str(OrderItemStatusEnum.PREPARING.value)
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_update_not_found(self, admin_client):
        url = f"v1/order_item/status/{uuid4()}"
        response = await admin_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
