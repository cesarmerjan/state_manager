from uuid import uuid4

import pytest

from src.schemas.state import StateUuidSchema
from src.services.state.delete import delete_state
from src.services.state.exceptions import (InvalidStateUuidType,
                                           InvalidUnitOfWorkType)
from tests.conftest import basic_types


def test_delete_state_service(unit_of_work, Repository):

    state_data = {"uuid": str(uuid4()), "payload": "data"}
    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        repository.set(state_data["uuid"], state_data["payload"])
        unit_of_work.commit()

    state_uuid = StateUuidSchema(uuid=state_data["uuid"])

    delete_state(unit_of_work, Repository, state_uuid)

    with unit_of_work:
        repository = Repository(unit_of_work.database_client)
        assert not repository.get(state_data["uuid"])


@pytest.mark.parametrize(
    "unit_of_work",
    basic_types,
)
def test_delete_state_service_unit_of_work_errors(unit_of_work, Repository):

    with pytest.raises(InvalidUnitOfWorkType):
        delete_state(unit_of_work, Repository, str(uuid4()))


@pytest.mark.parametrize(
    "state_uuid",
    basic_types,
)
def test_delete_state_service_state_uuid_errors(unit_of_work, Repository, state_uuid):

    with pytest.raises(InvalidStateUuidType):
        delete_state(unit_of_work, Repository, state_uuid)
