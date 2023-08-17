from fastapi import Depends

from src.app.controllers import UserController, AuthController
from src.app.repositories import UserRepository
from src.app.models import User
from src.core.database import get_db


class Factory:

    @staticmethod
    def get_user_controller(
            self,
            db: Depends = Depends(get_db)
    ) -> UserController:
        """
        Returns a UserController instance
        """
        return UserController(
            repository=UserRepository(model=User, database=db)
        )

    @staticmethod
    def get_auth_controller(
            self,
            db: Depends = Depends(get_db)
    ) -> UserController:
        """
        Returns a UserController instance
        """
        return AuthController(
            repository=UserRepository(model=User, database=db)
        )
