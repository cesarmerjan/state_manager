import uuid

from pydantic import BaseModel, validator


class StateUuidSchema(BaseModel):
    uuid: uuid.UUID

    @validator("uuid")
    def str_uuid(cls, value):
        return str(value)

    class Config:
        extra = "forbid"
