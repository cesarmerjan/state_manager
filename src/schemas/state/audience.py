from typing import List

from pydantic import BaseModel, validator

from src.extensions.host_validator import validate_hosts


class AudienceSchema(BaseModel):
    hosts: List[str]

    _hosts_validator = validator("hosts", allow_reuse=True)(validate_hosts)

    class Config:
        extra = "forbid"
