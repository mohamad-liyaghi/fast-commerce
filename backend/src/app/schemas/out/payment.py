from pydantic import BaseModel
from uuid import UUID
from src.app.schemas.base import BasePayment


class PaymentListOut(BasePayment):
    pass


class PaymentOrderOut(BaseModel):
    uuid: UUID


class PaymentRetrieveOut(BasePayment):
    order: PaymentOrderOut
