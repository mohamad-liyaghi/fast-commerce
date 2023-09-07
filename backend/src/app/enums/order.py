from enum import Enum


class OrderStatusEnum(Enum):
    PENDING_PAYMENT = "pending_payment"
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
