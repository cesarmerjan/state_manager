from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse

from src import services
from src.api.resources.dependencies import (get_repository,
                                            get_session_cookie_name,
                                            get_state_uuid, get_unit_of_work)
from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface


def register_delete_state_resource(router: APIRouter):
    @router.delete(
        "/",
        summary="Delete state",
        responses={
            202: {
                "content": {
                    "application/json": {"example": {"message": "State Deleted"}}
                },
                "description": "Success On Delete State",
            },
            400: {
                "content": {
                    "application/json": {
                        "example": {"message": "Not a valid session id"}
                    }
                },
                "description": "Bad session id cookie",
            },
            403: {
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Requester is not the audience of this state"
                        }
                    }
                },
                "description": "Requester origin isn't registered at the state audience",
            },
            404: {
                "content": {
                    "application/json": {
                        "example": {"message": "The state does not exist"}
                    }
                },
                "description": "State Not Found",
            },
        },
    )
    def delete_state(
        response: Response,
        unit_of_work: UnitOfWorkInterface = Depends(get_unit_of_work),
        Repository: RepositoryInterface = Depends(get_repository),
        state_uuid: str = Depends(get_state_uuid),
        session_cookie_name: str = Depends(get_session_cookie_name),
    ):
        """

        Use to delete the application state using a session id.

        - **session_id (string)**: session id cookie.

        """

        services.delete_state(unit_of_work, Repository, state_uuid)

        response = JSONResponse(
            {"message": "State Deleted"}, status_code=status.HTTP_202_ACCEPTED
        )

        response.delete_cookie(session_cookie_name)

        return response
