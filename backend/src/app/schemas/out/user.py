from pydantic import BaseModel, Field
from uuid import UUID


class CurrentUser(BaseModel):
    uuid: UUID = Field(None, description="User UUID")

    class Config:
        validate_assignment = True
