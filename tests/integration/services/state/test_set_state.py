from uuid import uuid4

import pytest

from src.entities.state import State
from src.services.encoder import decode_state
from src.services.signer import unsign_state
from src.services.state.exceptions import (InvalidStateType,
                                           InvalidUnitOfWorkType,
                                           MissingSecretKey)
from src.services.state.set import set_state
from tests.conftest import basic_types


def test_set_not_signed_state(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    set_state(unit_of_work, Repository, state, False)

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        state_claims = decode_state(repository.get(state.uuid))

    assert state_claims == state.claims


def test_set_signed_state(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    set_state(unit_of_work, Repository, state, True, "KEY")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        state_claims = decode_state(unsign_state(repository.get(state.uuid), "KEY"))

    assert state_claims == state.claims


@pytest.mark.parametrize(
    "unit_of_work",
    basic_types,
)
def test_set_state_service_unit_of_work_errors(unit_of_work, Repository):
    state = State({"data": "data"}, str(uuid4()), "service")

    with pytest.raises(InvalidUnitOfWorkType):
        set_state(unit_of_work, Repository, state)


@pytest.mark.parametrize(
    "state",
    basic_types,
)
def test_set_state_service_state_errors(unit_of_work, Repository, state):

    with pytest.raises(InvalidStateType):
        set_state(unit_of_work, Repository, state)


def test_get_state_service_missing_secret_key_error(unit_of_work, Repository):
    state = State({"data": "data"}, str(uuid4()), "service")
    with pytest.raises(MissingSecretKey):
        set_state(unit_of_work, Repository, state, True)
