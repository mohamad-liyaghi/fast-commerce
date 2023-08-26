from uuid import UUID
from datetime import datetime
from typing import List, Optional
from src.app.schemas.base import BaseProductCreate, BaseProduct


class ProductCreateOut(BaseProductCreate):
    uuid: UUID
    created_at: datetime


ProductListOut = Optional[List[BaseProduct]]
# TODO: Add uuid for this
