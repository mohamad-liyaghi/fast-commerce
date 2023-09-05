from fastapi import Depends
from src.app.controllers import (
    UserController,
    AuthController,
    VendorController,
    ProductController,
    CartController,
    OrderController,
)
from src.app.repositories import (
    UserRepository,
    VendorRepository,
    CartRepository,
    AuthRepository,
    ProductRepository,
    OrderRepository,
)
from src.app.models import User, Vendor, Product, Order
from src.core.database import get_db
from src.core.redis import get_redis


class Factory:
    """
    Factory class to create instances of controllers
    """

    @staticmethod
    def get_user_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> UserController:
        """
        Returns a UserController instance
        """
        return UserController(
            repository=UserRepository(
                model=User, database_session=db, redis_session=redis
            )
        )

    @staticmethod
    def get_auth_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> UserController:
        """
        Returns a UserController instance
        """
        return AuthController(
            repository=AuthRepository(
                model=User, database_session=db, redis_session=redis
            )
        )

    @staticmethod
    def get_vendor_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> VendorController:
        """
        Returns a VendorController instance
        """
        return VendorController(
            repository=VendorRepository(
                model=Vendor, database_session=db, redis_session=redis
            )
        )

    @staticmethod
    def get_product_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> ProductController:
        """
        Returns a ProductController instance
        """
        return ProductController(
            repository=ProductRepository(
                model=Product, database_session=db, redis_session=redis
            )
        )

    @staticmethod
    def get_cart_controller(redis: Depends = Depends(get_redis)) -> CartController:
        """
        Returns a CartController instance
        """
        return CartController(repository=CartRepository(redis_client=redis))

    @staticmethod
    def get_order_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> OrderController:
        """
        Returns a OrderController instance
        """
        return OrderController(
            repository=OrderRepository(
                model=Order, database_session=db, redis_session=redis
            )
        )
