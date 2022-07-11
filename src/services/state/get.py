from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state import StateUuidSchema
from src.services.encoder import decode_state
from src.services.signer import unsign_state

from .exceptions import (InvalidSecretKeyType, InvalidSignedStateType,
                         InvalidStateUuidType, InvalidUnitOfWorkType,
                         MissingSecretKey, StateNotFound)


def get_state(
    unit_of_work: UnitOfWorkInterface,
    Repository: RepositoryInterface,
    state_uuid: StateUuidSchema,
    signed_state: bool = False,
    secret_key: str = None,
) -> dict:
    """_summary_

    Args:
        unit_of_work (UnitOfWorkInterface): _description_
        Repository (RepositoryInterface): _description_
        state_uuid (StateUuidSchema): _description_
        signed_state (bool): _description_
        secret_key (str): _description_

    Raises:
        MissingSecretKey: _description_
        InvalidUnitOfWorkType: _description_
        InvalidStateUuidType: _description_
        InvalidSignedStateType: _description_
        InvalidSecretKeyType: _description_
        StateNotFound: _description_
        StringSignerException: _description_
        WebEncoderException: _description_
        RedisError: _description_

    Returns:
        dict: _description_
    """

    if signed_state and not secret_key:
        raise MissingSecretKey

    if not isinstance(unit_of_work, UnitOfWorkInterface):
        raise InvalidUnitOfWorkType

    if not isinstance(state_uuid, StateUuidSchema):
        raise InvalidStateUuidType

    if not isinstance(signed_state, bool):
        raise InvalidSignedStateType

    if not isinstance(secret_key, (str, type(None))) or secret_key == "":
        raise InvalidSecretKeyType

    with unit_of_work as uow:
        repository = Repository(uow.database_client)
        state = repository.get(state_uuid.uuid)

    if state:
        if signed_state:
            state = unsign_state(state, secret_key)

        state = decode_state(state)

    else:
        raise StateNotFound

    return state
