from typing import Optional

from pydantic import BaseModel


class TimeDeltaSchema(BaseModel):
    seconds: Optional[int]
    minutes: Optional[int]
    hours: Optional[int]
    days: Optional[int]

    class Config:
        extra = "forbid"
