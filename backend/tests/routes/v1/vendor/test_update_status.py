import pytest
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient
from src.app.enums import VendorStatusEnum


@pytest.mark.asyncio
class TestUpdateVendorStatusRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, accepted_vendor) -> None:
        self.client = client
        self.url = f"v1/vendor/status/{accepted_vendor.uuid}"
        self.data = {
            "status": VendorStatusEnum.REJECTED.value,
        }

    @pytest.mark.asyncio
    async def test_update_unauthorized(self) -> None:
        response = await self.client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_not_admin(self, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update(self, admin_client) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == self.data["status"]

    @pytest.mark.asyncio
    async def test_update_not_found(self, admin_client) -> None:
        response = await admin_client.put(f"v1/vendor/status/{uuid4()}", json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
