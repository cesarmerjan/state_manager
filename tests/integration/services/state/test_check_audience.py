from datetime import timedelta
from uuid import uuid4

import pytest

from src.entities.state import State
from src.schemas.state import RequesterSchema, StateUuidSchema
from src.services.encoder import encode_state
from src.services.signer import sign_encoded_state
from src.services.state.check_audience import check_if_is_the_state_audience
from src.services.state.exceptions import (InvalidRequesterType,
                                           InvalidStateUuidType,
                                           InvalidUnitOfWorkType,
                                           MissingSecretKey, NotTheAudience,
                                           StateNotFound)
from tests.conftest import basic_types


def test_check_not_signed_state(unit_of_work, Repository):

    localhost = "127.0.0.1"

    state = State(
        {"data": "data"}, str(uuid4()), "service", timedelta(seconds=30), [localhost]
    )

    requester = RequesterSchema(host=localhost)

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, encode_state(state))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    check_if_is_the_state_audience(unit_of_work, Repository, state_uuid, requester)


def test_check_signed_state(unit_of_work, Repository):

    localhost = "127.0.0.1"

    state = State(
        {"data": "data"}, str(uuid4()), "service", timedelta(seconds=30), [localhost]
    )

    requester = RequesterSchema(host=localhost)

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, sign_encoded_state(encode_state(state), "KEY"))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    check_if_is_the_state_audience(
        unit_of_work, Repository, state_uuid, requester, True, "KEY"
    )


def test_state_not_found(unit_of_work, Repository):

    state_uuid = StateUuidSchema(uuid=str(uuid4()))

    localhost = "127.0.0.1"
    requester = RequesterSchema(host=localhost)

    with pytest.raises(StateNotFound):
        check_if_is_the_state_audience(unit_of_work, Repository, state_uuid, requester)


def test_check_requester_not_allowed(unit_of_work, Repository):

    localhost = "127.0.0.1"

    state = State(
        {"data": "data"}, str(uuid4()), "service", timedelta(seconds=30), [localhost]
    )

    requester = RequesterSchema(host="other-origin.com")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, encode_state(state))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    with pytest.raises(NotTheAudience):
        check_if_is_the_state_audience(unit_of_work, Repository, state_uuid, requester)


@pytest.mark.parametrize(
    "unit_of_work",
    basic_types,
)
def test_check_audience_service_unit_of_work_errors(unit_of_work, Repository):
    with pytest.raises(InvalidUnitOfWorkType):
        check_if_is_the_state_audience(
            unit_of_work,
            Repository,
            StateUuidSchema(uuid=str(uuid4())),
            RequesterSchema(host="127.0.0.1"),
        )


@pytest.mark.parametrize(
    "state_uuid",
    basic_types,
)
def test_check_audience_service_state_uuid_errors(unit_of_work, Repository, state_uuid):

    with pytest.raises(InvalidStateUuidType):
        check_if_is_the_state_audience(
            unit_of_work, Repository, state_uuid, RequesterSchema(host="127.0.0.1")
        )


@pytest.mark.parametrize(
    "requester",
    basic_types,
)
def test_check_audience_service_requester_errors(unit_of_work, Repository, requester):
    with pytest.raises(InvalidRequesterType):
        check_if_is_the_state_audience(
            unit_of_work, Repository, StateUuidSchema(uuid=str(uuid4())), requester
        )


def test_check_audience_missing_secret_key_error(unit_of_work, Repository):
    localhost = "127.0.0.1"

    state = State(
        {"data": "data"}, str(uuid4()), "service", timedelta(seconds=30), [localhost]
    )

    requester = RequesterSchema(host=localhost)

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, sign_encoded_state(encode_state(state), "KEY"))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    with pytest.raises(MissingSecretKey):
        check_if_is_the_state_audience(
            unit_of_work, Repository, state_uuid, requester, True
        )
