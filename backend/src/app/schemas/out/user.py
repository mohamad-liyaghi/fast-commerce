from datetime import datetime
from src.app.schemas.base import UserBase


class UserOut(UserBase):
    is_admin: bool
    date_joined: datetime
