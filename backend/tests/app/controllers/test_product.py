import pytest
import asyncio
import uuid
from fastapi import HTTPException
from tests.utils.faker import create_product_credential


class TestProductController:
    @pytest.fixture(autouse=True)
    def setup(self, product_controller):
        self.data = asyncio.run(create_product_credential())
        self.controller = product_controller

    @pytest.mark.asyncio
    async def test_create_fails_by_rejected_vendor(self, user, rejected_vendor):
        with pytest.raises(HTTPException):
            await self.controller.create(
                request_user=user, request_vendor=rejected_vendor, data=self.data
            )

    @pytest.mark.asyncio
    async def test_create_by_accepted_owner(self, user, accepted_vendor):
        await self.controller.create(
            request_user=user, request_vendor=accepted_vendor, data=self.data
        )
        assert await self.controller.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_update_by_owner(self, user, product):
        await self.controller.update_product(
            uuid=product.uuid, request_user=user, data=self.data
        )
        assert await self.controller.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_update_fails_by_non_owner(self, admin, product):
        with pytest.raises(HTTPException):
            await self.controller.update_product(
                uuid=product.uuid, request_user=admin, data=self.data
            )

    @pytest.mark.asyncio
    async def test_update_not_found(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.update_product(
                uuid=uuid.uuid4(), request_user=admin, data=self.data
            )

    @pytest.mark.asyncio
    async def test_delete_by_owner(self, user, product):
        await self.controller.delete_product(uuid=product.uuid, request_user=user)
        assert await self.controller.retrieve(many=True, title=product.title) is None

    @pytest.mark.asyncio
    async def test_delete_fails_by_non_owner(self, admin, product):
        with pytest.raises(HTTPException):
            await self.controller.delete_product(uuid=product.uuid, request_user=admin)

    @pytest.mark.asyncio
    async def test_delete_not_found(self, admin):
        with pytest.raises(HTTPException):
            await self.controller.delete_product(uuid=uuid.uuid4(), request_user=admin)
