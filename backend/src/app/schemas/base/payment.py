from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BasePayment(BaseModel):
    uuid: UUID
    created_at: datetime
    amount: int
