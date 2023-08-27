from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from src.app.schemas.base import BaseProductCreate, BaseProduct


class ProductCreateOut(BaseProductCreate):
    uuid: UUID
    created_at: datetime


class ProductListOut(BaseModel):
    uuid: UUID
