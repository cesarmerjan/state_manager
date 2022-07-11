import uuid
from datetime import datetime, timedelta
from typing import List, Optional

from .exceptions import (InvalidAudienceType, InvalidIssuerType,
                         InvalidPayloadType, InvalidSubjectType,
                         InvalidTimeToExpireType)


class State:

    __slots__ = (
        "uuid",
        "creation_datetime",
        "_payload",
        "_subject",
        "_time_to_expire",
        "_issuer",
        "_audience",
    )

    DEFAULT_TIMEDELTA = timedelta(days=5)

    def __init__(
        self,
        payload: dict,
        subject: str,
        issuer: str,
        time_to_expire: Optional[timedelta] = None,
        audience: Optional[List[str]] = ["*"],
    ):
        self.uuid = str(uuid.uuid4())
        self.creation_datetime = datetime.utcnow()
        self._payload = None
        self.payload = payload
        self._subject = None
        self.subject = subject
        self._time_to_expire = None
        self.time_to_expire = time_to_expire
        self._issuer = None
        self.issuer = issuer
        self._audience = None
        self.audience = audience

    def __str__(self) -> str:
        return f"state: {self.uuid}"

    def __repr__(self) -> str:
        return f"State(uuid={self.uuid})"

    @property
    def payload(self) -> dict:
        return self._payload

    @payload.setter
    def payload(self, payload: dict) -> None:
        if not isinstance(payload, dict):
            raise InvalidPayloadType
        self._payload = payload

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, subject: str) -> None:
        if not isinstance(subject, str):
            raise InvalidSubjectType
        self._subject = subject

    @property
    def issuer(self) -> str:
        return self._issuer

    @issuer.setter
    def issuer(self, issuer: str) -> None:
        if not isinstance(issuer, str):
            raise InvalidIssuerType
        self._issuer = issuer

    @property
    def time_to_expire(self) -> timedelta:
        return self._time_to_expire

    @time_to_expire.setter
    def time_to_expire(self, time_to_expire: timedelta) -> None:
        if not isinstance(time_to_expire, timedelta) and time_to_expire is not None:
            raise InvalidTimeToExpireType
        self._time_to_expire = time_to_expire or self.DEFAULT_TIMEDELTA

    @property
    def audience(self) -> List[str]:
        return self._audience

    @audience.setter
    def audience(self, audience: List[str]) -> None:
        if not isinstance(audience, list):
            raise InvalidAudienceType
        if not all(isinstance(item, str) for item in audience):
            raise InvalidAudienceType
        self._audience = audience

    @property
    def seconds_to_expire(self) -> int:
        seconds = int(self.time_to_expire.total_seconds())
        return seconds

    @property
    def claims(self) -> dict:
        buffer = {}
        buffer["payload"] = {key: value for key, value in self.payload.items()}
        buffer["subject"] = self.subject
        buffer["issuer"] = self.issuer
        buffer["audience"] = self.audience
        return buffer

    @classmethod
    def instantiate_with_claims(
        cls, claims: dict, time_to_expire: Optional[timedelta] = None
    ) -> "State":
        sub = claims.pop("subject")
        issuer = claims.pop("issuer")
        audience = claims.pop("audience")
        state = cls(claims, sub, issuer, time_to_expire, audience)
        return state
