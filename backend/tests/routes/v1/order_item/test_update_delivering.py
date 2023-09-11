from fastapi import status
from uuid import uuid4
import pytest
from src.app.enums import OrderItemStatusEnum


class TestUpdateDeliveringItemRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, preparing_order_item) -> None:
        self.url = f"v1/order_item/status/{preparing_order_item.uuid}"
        self.order_item = preparing_order_item
        self.data = {
            "status": str(OrderItemStatusEnum.DELIVERING.value),
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_vendor(self, accepted_vendor, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_non_vendor(self, admin_client) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_already_delivering(
        self, authorized_client, delivering_order_item
    ):
        url = f"v1/order_item/status/{delivering_order_item.uuid}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert delivering_order_item.status == OrderItemStatusEnum.DELIVERING

    @pytest.mark.asyncio
    async def test_update_invalid_status(self, authorized_client):
        self.data["status"] = str(OrderItemStatusEnum.PREPARING.value)
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_update_not_found(self, authorized_client, accepted_vendor):
        url = f"v1/order_item/status/{uuid4()}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
