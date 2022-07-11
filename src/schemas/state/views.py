from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .audience import AudienceSchema
from .issuer import IssuerSchema
from .timedelta import TimeDeltaSchema


class StateView(BaseModel):
    payload: Dict[str, Union[str, List[str]]]
    subject: str
    issuer: IssuerSchema
    timeToExpire: Optional[TimeDeltaSchema]
    audience: Optional[AudienceSchema]

    class Config:
        extra = "forbid"
