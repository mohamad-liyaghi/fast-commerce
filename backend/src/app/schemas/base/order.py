from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    delivery_address: str = Field(..., min_length=1, max_length=255)
