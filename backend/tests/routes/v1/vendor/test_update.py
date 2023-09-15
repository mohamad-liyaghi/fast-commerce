import pytest
import asyncio
from uuid import uuid4
from fastapi import status
from httpx import AsyncClient
from tests.utils.faker import create_vendor_credential


@pytest.mark.asyncio
class TestUpdateVendorRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient, accepted_vendor) -> None:
        self.client = client
        self.url = f"v1/vendor/{accepted_vendor.uuid}"
        self.data = asyncio.run(create_vendor_credential())

    @pytest.mark.asyncio
    async def test_update_unauthorized(self) -> None:
        response = await self.client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_owner(self, authorized_client) -> None:
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["domain"] == self.data["domain"]

    @pytest.mark.asyncio
    async def test_update_not_found(self, authorized_client) -> None:
        response = await authorized_client.put(f"v1/vendor/{uuid4()}", json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_update_data_by_admin(self, admin_client) -> None:
        """Admins can only update status"""
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
