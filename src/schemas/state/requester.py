from typing import Optional

from pydantic import BaseModel, validator

from src.extensions.host_validator import validate_host


class RequesterSchema(BaseModel):
    host: str

    _host_validator = validator("host", allow_reuse=True)(validate_host)

    class Config:
        extra = "forbid"
