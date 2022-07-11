from datetime import timedelta

import pytest

from src.entities.state import State
from src.schemas.state import IssuerSchema, StateSchema
from src.services.state.create import create_state
from src.services.state.exceptions import (InvalidIssuerType,
                                           InvalidStateDataType)
from tests.conftest import basic_types


def test_create_state_without_defaults():
    payload = {"data": "data"}
    subject = "user_id"
    time_to_expire = {"seconds": 5}
    audience = {"hosts": ["127.0.0.1", "www.google.com", "other-service.io"]}
    state_schema = StateSchema(
        payload=payload, subject=subject, timeToExpire=time_to_expire, audience=audience
    )

    issuer = IssuerSchema(host="somehost.com")

    state = create_state(state_schema, issuer)

    assert isinstance(state, State)
    assert state.payload == payload
    assert state.subject == subject
    assert state.time_to_expire == timedelta(**time_to_expire)
    assert state.audience == audience["hosts"]
    assert state.issuer == issuer.host


def test_create_state_with_defaults():
    payload = {"data": "data"}
    subject = "user_id"
    state_schema = StateSchema(payload=payload, subject=subject)

    issuer = IssuerSchema(host="somehost.com")

    state = create_state(state_schema, issuer)

    assert isinstance(state, State)
    assert state.payload == payload
    assert state.subject == subject
    assert state.issuer == issuer.host
    assert state.time_to_expire == state.DEFAULT_TIMEDELTA
    assert state.audience == ["*"]


@pytest.mark.parametrize(
    "state_schema",
    basic_types,
)
def test_create_state_service_state_schema_errors(state_schema):

    with pytest.raises(InvalidStateDataType):
        create_state(state_schema, IssuerSchema(host="somehost.com"))


@pytest.mark.parametrize(
    "issuer",
    basic_types,
)
def test_create_state_service_issuer_errors(issuer):
    payload = {"data": "data"}
    subject = "user_id"
    state_schema = StateSchema(payload=payload, subject=subject)

    with pytest.raises(InvalidIssuerType):
        create_state(state_schema, issuer)
