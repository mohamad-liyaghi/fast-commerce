from enum import Enum


class OrderItemStatusEnum(Enum):
    PENDING_PAYMENT = "pending_payment"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
