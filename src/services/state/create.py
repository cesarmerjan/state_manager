from datetime import timedelta

from src.entities.state import State
from src.schemas.state import StateSchema
from src.schemas.state.issuer import IssuerSchema

from .exceptions import InvalidIssuerType, InvalidStateDataType


def create_state(state_data: StateSchema, issuer: IssuerSchema) -> State:
    """_summary_

    Args:
        state_data (StateSchema): _description_
        issuer (IssuerSchema): _description_

    Raises:
        InvalidStateDataType: _description_
        InvalidIssuerType: _description_

    Returns:
        State: _description_
    """

    if not isinstance(state_data, StateSchema):
        raise InvalidStateDataType

    if not isinstance(issuer, IssuerSchema):
        raise InvalidIssuerType

    state_data_dict = state_data.dict(exclude_unset=True)

    if state_data_dict.get("timeToExpire"):
        state_data_dict["time_to_expire"] = timedelta(
            **state_data.timeToExpire.dict(exclude_unset=True)
        )
        state_data_dict.pop("timeToExpire")

    if state_data_dict.get("audience"):
        state_data_dict["audience"] = state_data_dict["audience"]["hosts"]

    state = State(**state_data_dict, issuer=issuer.host)

    return state
