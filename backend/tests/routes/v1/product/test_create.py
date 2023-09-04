from fastapi import status
import pytest
from tests.utils.faker import create_product_credential
from src.app.enums import VendorStatusEnum


class TestCreateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = "v1/product/"

    @pytest.mark.asyncio
    async def test_create_unauthorized(self, client):
        credential = await create_product_credential()
        response = await client.post(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_no_vendor(self, authorized_client):
        credential = await create_product_credential()
        response = await authorized_client.post(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_create_rejected_vendor(self, authorized_client, rejected_vendor):
        """
        Test that a rejected vendor cannot create a product
        """
        credential = await create_product_credential()
        response = await authorized_client.post(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert rejected_vendor.status == VendorStatusEnum.REJECTED

    @pytest.mark.asyncio
    async def test_create_pending_vendor(self, authorized_client, pending_vendor):
        """
        Test that a pending vendor cannot create a product
        """
        credential = await create_product_credential()
        response = await authorized_client.post(self.url, json=credential)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert pending_vendor.status == VendorStatusEnum.PENDING

    @pytest.mark.asyncio
    async def test_create_with_accepted_vendor(
        self, authorized_client, accepted_vendor
    ):
        """
        Test that an accepted vendor can create a product
        """
        credential = await create_product_credential()
        response = await authorized_client.post(self.url, json=credential)
        assert response.status_code == status.HTTP_201_CREATED
        assert accepted_vendor.status == VendorStatusEnum.ACCEPTED

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
        assert accepted_vendor.status == VendorStatusEnum.ACCEPTED
