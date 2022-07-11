import pytest

from src.entities.state import State
from src.entities.state.exceptions import (InvalidAudienceType,
                                           InvalidIssuerType,
                                           InvalidPayloadType,
                                           InvalidSubjectType,
                                           InvalidTimeToExpireType)
from tests.conftest import basic_types


def test_state_creation(state_data: dict):

    state = State(**state_data)

    assert isinstance(state, State)

    assert state.payload == state_data["payload"]
    assert state.subject == state_data["subject"]
    assert state.issuer == state_data["issuer"]
    assert state.time_to_expire == state_data["time_to_expire"]
    assert state.audience == state_data["audience"]

    assert isinstance(state.seconds_to_expire, int)

    del state_data["time_to_expire"]

    assert state.claims == state_data


def test_state_creation_with_default(state_data: dict):

    del state_data["time_to_expire"]
    del state_data["audience"]

    state = State(**state_data)

    assert isinstance(state, State)

    assert state.payload == state_data["payload"]
    assert state.subject == state_data["subject"]
    assert state.issuer == state_data["issuer"]
    assert state.time_to_expire == State.DEFAULT_TIMEDELTA
    assert state.audience == ["*"]


def test_state_creation_with_claims(state_data: dict):

    time_to_expire = state_data.pop("time_to_expire")

    state = State.instantiate_with_claims(state_data, time_to_expire)

    assert isinstance(state, State)


def test_state_claims(state_data):
    state = State(**state_data)

    del state_data["time_to_expire"]

    assert state.claims == state_data


@pytest.mark.parametrize("payload", [i for i in basic_types if not isinstance(i, dict)])
def test_state_payload_set_error(payload, state_data: dict):

    with pytest.raises(InvalidPayloadType):
        State(
            payload=payload,
            subject=state_data["subject"],
            issuer=state_data["issuer"],
            time_to_expire=state_data["time_to_expire"],
            audience=state_data["audience"],
        )


@pytest.mark.parametrize("subject", [i for i in basic_types if not isinstance(i, str)])
def test_state_subject_set_error(subject, state_data: dict):

    with pytest.raises(InvalidSubjectType):
        State(
            payload=state_data["payload"],
            subject=subject,
            issuer=state_data["issuer"],
            time_to_expire=state_data["time_to_expire"],
            audience=state_data["audience"],
        )


@pytest.mark.parametrize(
    "issuer",
    [i for i in basic_types if not isinstance(i, str)],
)
def test_state_issuer_set_error(issuer, state_data: dict):

    with pytest.raises(InvalidIssuerType):
        State(
            payload=state_data["payload"],
            subject=state_data["subject"],
            issuer=issuer,
            time_to_expire=state_data["time_to_expire"],
            audience=state_data["audience"],
        )


@pytest.mark.parametrize(
    "time_to_expire",
    [i for i in basic_types if i is not None],
)
def test_state_time_to_expire_set_error(time_to_expire, state_data: dict):

    with pytest.raises(InvalidTimeToExpireType):
        State(
            payload=state_data["payload"],
            subject=state_data["subject"],
            issuer=state_data["issuer"],
            time_to_expire=time_to_expire,
            audience=state_data["audience"],
        )


@pytest.mark.parametrize(
    "audience",
    [
        1,
        1.2,
        "string",
        {},
        set([]),
        lambda: "function",
        type("MyClass", (object,), {}),
        True,
        ["string", True],
        ["string", 1],
        ["string", 1.2],
        ["string", {}],
        ["string", []],
        ["string", set([])],
        ["string", lambda: "function"],
        ["string", type("MyClass", (object,), {})],
    ],
)
def test_state_audience_set_error(audience, state_data: dict):

    with pytest.raises(InvalidAudienceType):
        State(
            payload=state_data["payload"],
            subject=state_data["subject"],
            issuer=state_data["issuer"],
            time_to_expire=state_data["time_to_expire"],
            audience=audience,
        )
