from uuid import uuid4

import pytest

from src.entities.state import State
from src.schemas.state import StateUuidSchema
from src.services.encoder import encode_state
from src.services.signer import sign_encoded_state
from src.services.state.exceptions import (InvalidStateUuidType,
                                           InvalidUnitOfWorkType,
                                           MissingSecretKey, StateNotFound)
from src.services.state.get import get_state
from tests.conftest import basic_types


def test_get_not_signed_state(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, encode_state(state))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    state_claims = get_state(unit_of_work, Repository, state_uuid, False)

    assert state_claims == state.claims


def test_get_signed_state(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, sign_encoded_state(encode_state(state), "KEY"))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    state_claims = get_state(unit_of_work, Repository, state_uuid, True, "KEY")

    assert state_claims == state.claims


def test_state_not_found(unit_of_work, Repository):

    state_uuid = StateUuidSchema(uuid=str(uuid4()))

    with pytest.raises(StateNotFound):
        get_state(unit_of_work, Repository, state_uuid)


@pytest.mark.parametrize(
    "unit_of_work",
    basic_types,
)
def test_get_state_service_unit_of_work_errors(unit_of_work, Repository):

    with pytest.raises(InvalidUnitOfWorkType):
        get_state(unit_of_work, Repository, str(uuid4()))


@pytest.mark.parametrize(
    "state_uuid",
    basic_types,
)
def test_get_state_service_state_uuid_errors(unit_of_work, Repository, state_uuid):

    with pytest.raises(InvalidStateUuidType):
        get_state(unit_of_work, Repository, state_uuid)


def test_get_state_service_missing_secret_key_error(unit_of_work, Repository):
    with pytest.raises(MissingSecretKey):
        get_state(unit_of_work, Repository, StateUuidSchema(uuid=uuid4()), True)
