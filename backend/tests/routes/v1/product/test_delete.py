import pytest
from uuid import uuid4
from fastapi import status


@pytest.mark.asyncio
class TestDeleteProductRoute:
    @pytest.fixture(autouse=True)
    def setup_method(self, product) -> None:
        self.url = f"v1/product/{product.uuid}"
        self.product = product

    @pytest.mark.asyncio
    async def test_delete_unauthenticated(self, client) -> None:
        """Should return 401 if user is not authenticated."""
        response = await client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_delete_by_other_user(self, admin_client, admin):
        """Should return 403 if user is not the owner of the product."""
        response = await admin_client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert self.product.user_id != admin.id

    @pytest.mark.asyncio
    async def test_delete_by_owner(self, authorized_client, user):
        response = await authorized_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.product.user_id == user.id

    @pytest.mark.asyncio
    async def test_delete_not_found(self, authorized_client):
        """Should return 404 if product does not exist."""
        url = f"v1/product/{uuid4()}"
        response = await authorized_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
