from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state import RequesterSchema, StateUuidSchema
from src.services.encoder import decode_state
from src.services.signer import unsign_state

from .exceptions import (InvalidRequesterType, InvalidSecretKeyType,
                         InvalidSignedStateType, InvalidStateUuidType,
                         InvalidUnitOfWorkType, MissingSecretKey,
                         NotTheAudience, StateNotFound)


def check_if_is_the_state_audience(
    unit_of_work: UnitOfWorkInterface,
    Repository: RepositoryInterface,
    state_uuid: StateUuidSchema,
    requester: RequesterSchema,
    signed_state: bool = False,
    secret_key: str = None,
) -> None:

    if signed_state and not secret_key:
        raise MissingSecretKey

    if not isinstance(unit_of_work, UnitOfWorkInterface):
        raise InvalidUnitOfWorkType

    if not isinstance(state_uuid, StateUuidSchema):
        raise InvalidStateUuidType

    if not isinstance(requester, RequesterSchema):
        raise InvalidRequesterType

    if not isinstance(signed_state, bool):
        raise InvalidSignedStateType

    if not isinstance(secret_key, (str, type(None))) or secret_key == "":
        raise InvalidSecretKeyType

    with unit_of_work as uow:
        repository = Repository(uow.database_client)
        state = repository.get(state_uuid.uuid)

    if not state:
        raise StateNotFound

    if state:
        if signed_state:
            state = unsign_state(state, secret_key)

        state = decode_state(state)

    if requester.host not in state["audience"] and "*" not in state["audience"]:
        raise NotTheAudience
