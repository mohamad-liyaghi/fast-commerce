from fastapi import status
from faker import Faker
from datetime import datetime, timedelta
import pytest
from httpx import AsyncClient
from src.app.models import VendorStatus

faker = Faker()  # TODO: Create a single instance of faker


class TestCreateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/product/"

    @pytest.mark.asyncio
    async def test_empty_list(self, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_non_empty_list(self, product, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
