from uuid import UUID
from datetime import datetime
from src.app.schemas.base import BaseProduct


class ProductCreateOut(BaseProduct):
    uuid: UUID
    created_at: datetime
