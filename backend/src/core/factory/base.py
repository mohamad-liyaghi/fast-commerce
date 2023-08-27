from fastapi import Depends
from src.app.controllers import (
    UserController,
    AuthController,
    VendorController,
    ProductController,
)
from src.app.repositories import UserRepository, VendorRepository
from src.app.models import User, Vendor, Product
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
            repository=UserRepository(model=User, database=db, redis=redis)
        )

    @staticmethod
    def get_auth_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> UserController:
        """
        Returns a UserController instance
        """
        return AuthController(
            repository=UserRepository(model=User, database=db, redis=redis)
        )

    @staticmethod
    def get_vendor_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> VendorController:
        """
        Returns a VendorController instance
        """
        return VendorController(
            repository=VendorRepository(model=Vendor, database=db, redis=redis)
        )

    @staticmethod
    def get_product_controller(
        db: Depends = Depends(get_db), redis: Depends = Depends(get_redis)
    ) -> ProductController:
        """
        Returns a ProductController instance
        """
        return ProductController(
            repository=VendorRepository(model=Product, database=db, redis=redis)
        )
