from fastapi import status
from faker import Faker
import pytest


faker = Faker()  # TODO: Create a single instance of faker


class TestUpdateProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, product) -> None:
        self.url = f"v1/product/{product.uuid}"
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
        self.product = product

    @pytest.mark.asyncio
    async def test_update_unauthorized(self, client) -> None:
        response = await client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_update_by_other_user(self, admin_client, admin) -> None:
        response = await admin_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert admin != self.product.user_id

    @pytest.mark.asyncio
    async def test_update_by_vendor(self, authorized_client, user):
        response = await authorized_client.put(self.url, json=self.data)
        assert response.status_code == status.HTTP_200_OK
        assert user.id == self.product.user_id

    @pytest.mark.asyncio
    async def test_update_not_found(self, authorized_client):
        url = f"v1/product/{faker.uuid4()}"
        response = await authorized_client.put(url, json=self.data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
