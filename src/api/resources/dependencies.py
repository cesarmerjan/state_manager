from fastapi import Cookie, Depends, HTTPException, Request, status
from pydantic import ValidationError

from src import services
from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state import RequesterSchema, StateUuidSchema
from src.services.state.exceptions import NotTheAudience, StateNotFound


async def get_unit_of_work(resquest: Request) -> UnitOfWorkInterface:
    """
    Get contexted unit_of_work

    Args:
        resquest (Request): Fastapi request

    Returns:
        UnitOfWorkInterface: contexted unit_of_work
    """
    return resquest.state.DATABASE.get_unit_of_work()


async def get_repository(resquest: Request) -> RepositoryInterface:
    """
    Get Repository

    Args:
        resquest (Request): Fastapi request

    Returns:
        RepositoryInterface: RepositoryInterface
    """
    return resquest.state.DATABASE.get_repository()


async def get_secret_key(resquest: Request) -> str:
    """
    Get application secret_key

    Args:
        resquest (Request): Fastapi request

    Returns:
        str: application secret_key
    """
    return resquest.state.SECRET_KEY


async def get_sign_state(resquest: Request) -> bool:
    """
    Get if application have to sign the state

    Args:
        resquest (Request): Fastapi request

    Returns:
        bool: application sign_state
    """
    return resquest.state.SIGN_STATE


async def get_session_cookie_name(resquest: Request) -> str:
    """
    Get application session cookie name

    Args:
        resquest (Request): Fastapi request

    Returns:
        str: sesseion cookie name
    """
    return resquest.state.SESSION_COOKIE_NAME


async def get_api_key(resquest: Request) -> str:
    """
    Get application session cookie name

    Args:
        resquest (Request): Fastapi request

    Returns:
        str: sesseion cookie name
    """
    return resquest.state.API_KEY


async def validate_session_id(
    request: Request, session_cookie_name: str = Depends(get_session_cookie_name)
) -> StateUuidSchema:
    """_summary_

    Args:
        session_id (str): _description_. Defaults to Cookie(None).

    Raises:
        HTTPException: _description_

    Returns:
        StateUuidSchema: _description_
    """

    session_id: Cookie(str) = request.cookies.get(session_cookie_name)

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing session cookie"
        )

    try:
        state_uuid = StateUuidSchema(uuid=session_id)
    except ValidationError as error:
        msg = ""
        for e in error.errors():
            msg += f"Session {error.errors()[0]['loc'][0]} {error.errors()[0]['msg']}."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    return state_uuid


def get_state_uuid(
    request: Request,
    unit_of_work: UnitOfWorkInterface = Depends(get_unit_of_work),
    Repository: RepositoryInterface = Depends(get_repository),
    state_uuid: str = Depends(validate_session_id),
) -> StateUuidSchema:
    """_summary_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        StateUuidSchema: _description_
    """

    requester = RequesterSchema(host=str(request.client.host))
    try:
        services.check_if_is_the_state_audience(
            unit_of_work, Repository, state_uuid, requester
        )
    except StateNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    except NotTheAudience as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error.message)

    return state_uuid
