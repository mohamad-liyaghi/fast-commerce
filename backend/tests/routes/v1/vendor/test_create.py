from fastapi import status
from faker import Faker
from datetime import datetime, timedelta
import pytest
from httpx import AsyncClient
from src.app.models import VendorStatusEnum

faker = Faker()  # TODO: Create a single instance of faker


class TestCreateVendorRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient) -> None:
        self.client = client
        self.url = f"v1/vendor/"
        self.data = {
            "name": faker.company(),
            "description": faker.paragraph(),
            "address": faker.address(),
            "domain": faker.domain_name(),
        }

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create(self, authorized_client):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED

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
        self, authorized_client, rejected_vendor, vendor_controller
    ):
        reviewed_at = datetime.utcnow() - timedelta(days=11)
        await vendor_controller.repository.update(
            rejected_vendor, reviewed_at=reviewed_at
        )
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert rejected_vendor.status == VendorStatusEnum.REJECTED
