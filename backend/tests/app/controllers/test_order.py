import pytest
from fastapi import HTTPException
from src.app.enums import OrderStatusEnum


class TestOrderController:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        order_controller,
        cart,
        order_item_controller,
        cart_controller,
        product_controller,
    ):
        self.controller = order_controller
        self.order_item_controller = order_item_controller
        self.cart_controller = cart_controller
        self.product_controller = product_controller
        self.cart = cart

    @pytest.mark.asyncio
    async def test_create_order(self, admin):
        await self.controller.create_order(
            request_user=admin,
            order_item_controller=self.order_item_controller,
            cart_controller=self.cart_controller,
            cart=self.cart,
            product_controller=self.product_controller,
            delivery_address="test address",
        )
        assert await self.controller.retrieve(many=True) is not None

    @pytest.mark.asyncio
    async def test_create_empty_cart(self, admin):
        self.cart = {}
        with pytest.raises(HTTPException):
            await self.controller.create_order(
                request_user=admin,
                order_item_controller=self.order_item_controller,
                cart_controller=self.cart_controller,
                cart=self.cart,
                product_controller=self.product_controller,
                delivery_address="test address",
            )

    @pytest.mark.asyncio
    async def test_order_price(self, admin, product):
        order = await self.controller.create_order(
            request_user=admin,
            order_item_controller=self.order_item_controller,
            cart_controller=self.cart_controller,
            cart=self.cart,
            product_controller=self.product_controller,
            delivery_address="test address",
        )

        assert order.total_price == product.price

    @pytest.mark.asyncio
    async def test_set_paid(self, order):
        order = await self.controller.set_paid(order=order)
        assert order.status == OrderStatusEnum.PREPARING

    @pytest.mark.asyncio
    async def test_set_paid_twice(self, order):
        order = await self.controller.set_paid(order=order)
        with pytest.raises(HTTPException):
            await self.controller.set_paid(order=order)

    @pytest.mark.asyncio
    async def test_set_delivering(self, paid_order, admin):
        order = await self.controller.set_delivering(
            order=paid_order, request_user=admin
        )
        assert order.status == OrderStatusEnum.DELIVERING

    @pytest.mark.asyncio
    async def test_set_delivering_as_user(self, paid_order, user):
        with pytest.raises(HTTPException):
            await self.controller.set_delivering(order=paid_order, request_user=user)

    @pytest.mark.asyncio
    async def test_set_delivering_twice(self, delivering_order, admin):
        with pytest.raises(HTTPException):
            await self.controller.set_delivering(
                order=delivering_order, request_user=admin
            )

    @pytest.mark.asyncio
    async def test_set_delivered(self, delivering_order, admin):
        order = await self.controller.set_delivered(
            order=delivering_order, request_user=admin
        )
        assert order.status == OrderStatusEnum.DELIVERED

    @pytest.mark.asyncio
    async def test_set_delivered_as_user(self, delivering_order, user):
        with pytest.raises(HTTPException):
            await self.controller.set_delivered(
                order=delivering_order, request_user=user
            )

    @pytest.mark.asyncio
    async def test_set_delivered_twice(self, delivered_order, admin):
        with pytest.raises(HTTPException):
            await self.controller.set_delivered(
                order=delivered_order, request_user=admin
            )
