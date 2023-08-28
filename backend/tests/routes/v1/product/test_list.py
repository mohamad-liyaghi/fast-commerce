from fastapi import status
import pytest
from httpx import AsyncClient


class TestCreateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = f"v1/product/"

    @pytest.mark.asyncio
    async def test_empty_list(
        self, client: AsyncClient, product, product_controller
    ) -> None:
        await product_controller.repository.delete(product)
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_non_empty_list(self, product, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert product is not None
