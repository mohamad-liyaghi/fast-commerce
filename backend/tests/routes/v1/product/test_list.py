from fastapi import status
import pytest
from httpx import AsyncClient


class TestListProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.url = "v1/product/"

    @pytest.mark.asyncio
    async def test_empty_list(
        self, client: AsyncClient, product, product_controller, user
    ) -> None:
        await product_controller.repository.delete_product(product, request_user=user)
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None

    @pytest.mark.asyncio
    async def test_non_empty_list(self, product, client: AsyncClient) -> None:
        response = await client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert product is not None

    @pytest.mark.asyncio
    async def test_filter_title(self, product, authorized_client) -> None:
        response = await authorized_client.get(self.url + f"?title={product.title}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    @pytest.mark.asyncio
    async def test_filter_title_not_exist(self, authorized_client) -> None:
        response = await authorized_client.get(self.url + "?title=not_exists")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() is None
