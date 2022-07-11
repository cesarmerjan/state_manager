from fastapi import APIRouter, Body, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src import services
from src.api.resources.dependencies import (get_repository, get_secret_key,
                                            get_session_cookie_name,
                                            get_sign_state, get_unit_of_work)
from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state import IssuerSchema, StateSchema


def register_post_state_resource(router: APIRouter):
    @router.post(
        "/",
        summary="Set state",
        responses={
            200: {
                "content": {"application/json": {"example": {"message": "State set"}}},
                "description": "Success On Set State",
            },
            500: {
                "content": {"application/json": {"example": {"message": "..."}}},
                "description": "Internal server error",
            },
        },
    )
    def post_state(
        request: Request,
        response: Response,
        unit_of_work: UnitOfWorkInterface = Depends(get_unit_of_work),
        Repository: RepositoryInterface = Depends(get_repository),
        state_data: StateSchema = Body(...),
        sign_state: bool = Depends(get_sign_state),
        secret_key: str = Depends(get_secret_key),
        session_cookie_name: str = Depends(get_session_cookie_name),
    ):
        """

        Use to set the application state.

        - **payload (object)**: The state payload.
        - **subject (string)**: The state subject, usually the user's uuid.
        - **timeToExpire (TimeDeltaSchema)**: The time for state to expire.
        - **audience (AudienceSchema)**: The list of hosts that will be able to access the state.

        """

        try:
            issuer = IssuerSchema(host=str(request.client.host))
        except ValidationError as error:
            response = JSONResponse(
                {"message": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:

            state = services.create_state(state_data, issuer)

            services.set_state(unit_of_work, Repository, state, sign_state, secret_key)

            response = JSONResponse(
                {"message": "State set"}, status_code=status.HTTP_201_CREATED
            )
            response.set_cookie(
                key=session_cookie_name,
                value=state.uuid,
                httponly=True,
                expires=state.seconds_to_expire,
            )
        except Exception as error:
            response = JSONResponse(
                {"message": str(error)}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response
