from pydantic import BaseModel, Field


class CartBase(BaseModel):
    quantity: int = Field(1, ge=1, le=10)
