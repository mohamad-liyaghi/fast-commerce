from fastapi import status
import pytest
import asyncio
from httpx import AsyncClient
from src.app.enums import VendorStatusEnum
from tests.utils.faker import create_vendor_credential


class TestCreateVendorRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient) -> None:
        self.client = client
        self.url = "v1/vendor/"
        self.data = asyncio.run(create_vendor_credential())

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_pending_exists(self, authorized_client, pending_vendor):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert pending_vendor.status == VendorStatusEnum.PENDING

    @pytest.mark.asyncio
    async def test_create_accepted_exists(self, authorized_client, accepted_vendor):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert accepted_vendor.status == VendorStatusEnum.ACCEPTED

    @pytest.mark.asyncio
    async def test_create_rejected_exists(self, authorized_client, rejected_vendor):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert rejected_vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_create_old_rejected_exist(
        self, authorized_client, old_rejected_vendor
    ):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert old_rejected_vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_create(self, authorized_client):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
