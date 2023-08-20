from datetime import datetime
from src.app.schemas.base import UserBase


class ProfileOut(UserBase):
    is_admin: bool
    date_joined: datetime
