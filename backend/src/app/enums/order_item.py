from enum import Enum


class OrderItemStatusEnum(Enum):
    PREPARING = "preparing"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
