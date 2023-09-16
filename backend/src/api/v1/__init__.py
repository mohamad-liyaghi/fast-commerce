from fastapi import APIRouter
from .auth import router as auth_router
from .user import router as user_router
from .vendor import router as vendor_router
from .product import router as product_router
from .cart import router as cart_router
from .order import router as order_router
from .order_item import router as order_item_router
from .payment import router as payment_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(user_router, prefix="/user")
v1_router.include_router(vendor_router, prefix="/vendor")
v1_router.include_router(product_router, prefix="/product")
v1_router.include_router(cart_router, prefix="/cart")
v1_router.include_router(order_router, prefix="/order")
v1_router.include_router(order_item_router, prefix="/order_item")
v1_router.include_router(payment_router, prefix="/payment")
