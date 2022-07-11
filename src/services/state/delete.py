from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state.uuid import StateUuidSchema

from .exceptions import InvalidStateUuidType, InvalidUnitOfWorkType


def delete_state(
    unit_of_work: UnitOfWorkInterface,
    Repository: RepositoryInterface,
    state_uuid: StateUuidSchema,
) -> None:
    """_summary_

    Args:
        unit_of_work (UnitOfWorkInterface): _description_
        Repository (RepositoryInterface): _description_
        state_uuid (StateUuidSchema): _description_

    Raises:
        InvalidUnitOfWorkType: _description_
        InvalidStateUuidType: _description_
        RedisError: _description_
    """
    if not isinstance(unit_of_work, UnitOfWorkInterface):
        raise InvalidUnitOfWorkType

    if not isinstance(state_uuid, StateUuidSchema):
        raise InvalidStateUuidType

    with unit_of_work as uow:
        repository = Repository(uow.database_client)
        repository.delete(state_uuid.uuid)
        uow.commit()
