from typing import Optional

from pydantic import BaseModel, validator

from src.extensions.host_validator import validate_host


def optional_host_validator(host: Optional[str]) -> str:
    if host is None or host == "":
        return "unknown"
    else:
        return validate_host(host)


class IssuerSchema(BaseModel):
    host: Optional[str]

    _host_validator = validator("host", allow_reuse=True)(optional_host_validator)

    class Config:
        extra = "forbid"
