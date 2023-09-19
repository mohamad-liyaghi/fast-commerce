from pydantic import BaseModel, Field
from typing import Dict, Any


class BaseProduct(BaseModel):
    title: str = Field(max_length=120)
    description: str = Field(max_length=300)
    price: int = Field(gt=0, lt=1_000_000)


class BaseProductSpecs(BaseProduct):
    specs: Dict[str, Any] = Field(default={})
    is_available: bool = Field(default=True)
