from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.entities.state.main import State
from src.services.encoder import encode_state
from src.services.signer import sign_encoded_state

from .exceptions import (InvalidSecretKeyType, InvalidSignStateType,
                         InvalidStateType, InvalidUnitOfWorkType,
                         MissingSecretKey)


def set_state(
    unit_of_work: UnitOfWorkInterface,
    Repository: RepositoryInterface,
    state: State,
    sign_state: bool = False,
    secret_key: str = None,
) -> None:
    """_summary_

    Args:
        unit_of_work (UnitOfWorkInterface): _description_
        Repository (RepositoryInterface): _description_
        state (State): _description_
        sign_state (bool): _description_
        secret_key(str): _description_

    Raises:
        MissingSecretKey: _description_
        InvalidUnitOfWorkType: _description_
        InvalidStateType: _description_
        InvalidSignStateType: _description_
        InvalidSecretKeyType: _description_
        StringSignerException: _description_
        WebEncoderException: _description_
        RedisError: _description_

    """

    if sign_state and not secret_key:
        raise MissingSecretKey

    if not isinstance(unit_of_work, UnitOfWorkInterface):
        raise InvalidUnitOfWorkType

    if not isinstance(state, State):
        raise InvalidStateType

    if not isinstance(sign_state, bool):
        raise InvalidSignStateType

    if not isinstance(secret_key, (str, type(None))) or secret_key == "":
        raise InvalidSecretKeyType

    with unit_of_work as uow:

        state_claims = encode_state(state)

        if sign_state:
            state_claims = sign_encoded_state(state_claims, secret_key)

        repository = Repository(uow.database_client)

        repository.set(state.uuid, state_claims)
        repository.expire(state.uuid, state.time_to_expire)
        uow.commit()
