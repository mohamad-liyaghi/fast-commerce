from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any, List


class CartListOut(BaseModel):
    product_uuid: UUID
    metadata: Dict[str, Any]
