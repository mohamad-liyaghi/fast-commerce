from fastapi import status
from faker import Faker
from datetime import datetime, timedelta
import pytest
from httpx import AsyncClient
from src.app.models import VendorStatus

faker = Faker()  # TODO: Create a single instance of faker


class TestCreateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, client: AsyncClient) -> None:
        self.client = client
        self.url = f"v1/product/"
        self.data = {
            "title": faker.name(),
            "description": faker.text(),
            "price": 1234,
            "specs": {
                "color": faker.color_name(),
                "size": "M",
                "weight": str(faker.pydecimal()),
            },
        }

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, client):
        response = await client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_no_vendor(self, authorized_client):
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_rejected_vendor(self, authorized_client, rejected_vendor):
        """
        Test that a rejected vendor cannot create a product
        """
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_pending_vendor(self, authorized_client, pending_vendor):
        """
        Test that a pending vendor cannot create a product
        """
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_with_accepted_vendor(
        self, authorized_client, accepted_vendor
    ):
        """
        Test that an accepted vendor can create a product
        """
        response = await authorized_client.post(self.url, json=self.data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.asyncio
    async def test_create_invalid_data(self, authorized_client, accepted_vendor):
        """
        Test that an accepted vendor cannot create a product with invalid data
        :param authorized_client:
        :param accepted_vendor:
        :return:
        """
        invalid_data = {}
        response = await authorized_client.post(self.url, json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
