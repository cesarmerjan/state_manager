import json
from uuid import uuid4

import pytest

from src.entities.state import State
from src.schemas.state import StateUuidSchema
from src.services.state.exceptions import (InvalidStateUuidType,
                                           InvalidUnitOfWorkType,
                                           StateNotFound)
from src.services.state.status import state_status
from tests.conftest import basic_types


def test_get_signed_state(unit_of_work, Repository):

    state = State({"data": "data"}, str(uuid4()), "service")

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state.uuid, json.dumps(state.claims))
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state.uuid)

    assert state_status(unit_of_work, Repository, state_uuid)


def test_state_not_found(unit_of_work, Repository):

    state_uuid = StateUuidSchema(uuid=str(uuid4()))

    with pytest.raises(StateNotFound):
        state_status(unit_of_work, Repository, state_uuid)


@pytest.mark.parametrize(
    "unit_of_work",
    basic_types,
)
def test_state_state_service_unit_of_work_errors(unit_of_work, Repository):

    state_uuid = StateUuidSchema(uuid=uuid4())

    with pytest.raises(InvalidUnitOfWorkType):
        state_status(unit_of_work, Repository, state_uuid)


@pytest.mark.parametrize(
    "state_uuid",
    basic_types,
)
def test_state_state_service_state_uuid_errors(unit_of_work, Repository, state_uuid):

    with pytest.raises(InvalidStateUuidType):
        state_status(unit_of_work, Repository, state_uuid)
