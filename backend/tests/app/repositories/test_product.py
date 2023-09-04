import pytest
from src.app.repositories import ProductRepository
from src.app.models import Product
from src.core.exceptions import ProductOwnerRequired, AcceptedVendorRequired
from tests.utils.faker import create_product_credential


class TestAuthRepository:
    @pytest.fixture(autouse=True)
    def setup(self, get_test_db, get_test_redis):
        self.repository = ProductRepository(
            model=Product, database_session=get_test_db, redis_session=get_test_redis
        )

    @pytest.mark.asyncio
    async def test_create(self, user, accepted_vendor):
        data = await create_product_credential()
        product = await self.repository.create(
            request_user=user, request_vendor=accepted_vendor, **data
        )
        assert product.user_id == user.id

    @pytest.mark.asyncio
    async def test_create_pending_vendor(self, user, pending_vendor):
        with pytest.raises(AcceptedVendorRequired):
            await self.repository.create(
                request_user=user, request_vendor=pending_vendor, data={}
            )

    @pytest.mark.asyncio
    async def test_create_rejected_vendor(self, user, rejected_vendor):
        with pytest.raises(AcceptedVendorRequired):
            await self.repository.create(
                request_user=user, request_vendor=rejected_vendor, data={}
            )

    @pytest.mark.asyncio
    async def test_update(self, user, product):
        product = await self.repository.update(
            product, request_user=user, data={"title": "new title"}
        )
        assert product.title == "new title"

    @pytest.mark.asyncio
    async def test_update_by_non_owner(self, admin, product):
        with pytest.raises(ProductOwnerRequired):
            await self.repository.update(product, request_user=admin, data={})

    @pytest.mark.asyncio
    async def test_delete(self, user, product):
        product = await self.repository.delete(product, request_user=user)
        assert product is None

    @pytest.mark.asyncio
    async def test_delete_by_non_owner(self, admin, product):
        with pytest.raises(ProductOwnerRequired):
            await self.repository.delete(product, request_user=admin)
