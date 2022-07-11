from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src import services
from src.api.resources.dependencies import (get_repository, get_state_uuid,
                                            get_unit_of_work)
from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface


def register_state_status_resource(router: APIRouter):
    @router.get(
        "/status",
        summary="Get state",
        responses={
            200: {
                "content": {"application/json": {"example": {"message": "OK"}}},
                "description": "Returns the state in json format",
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
    def state_status(
        unit_of_work: UnitOfWorkInterface = Depends(get_unit_of_work),
        Repository: RepositoryInterface = Depends(get_repository),
        state_uuid: str = Depends(get_state_uuid),
    ):
        """

        Use to check if the application state exists.
        This method ignores the state audience.

        - **session_id (string)**: session id cookie.

        """

        services.state_status(unit_of_work, Repository, state_uuid)
        response = JSONResponse({"message": "OK"}, status.HTTP_200_OK)

        return response
