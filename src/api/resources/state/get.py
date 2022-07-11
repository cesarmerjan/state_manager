from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src import services
from src.api.resources.dependencies import (get_repository, get_secret_key,
                                            get_sign_state, get_state_uuid,
                                            get_unit_of_work)
from src.database.interfaces import RepositoryInterface, UnitOfWorkInterface
from src.schemas.state import StateView


def register_get_state_resource(router: APIRouter):
    @router.get(
        "/",
        response_model=StateView,
        summary="Get state",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "example": {
                            "payload": {
                                "authentication": "LOGGED",
                                "permissions": ["add_user", "delete_user"],
                                "user_name": "AUser",
                            },
                            "subject": "1730b54d-5842-4675-a1f9-0d6fe0703557",
                            "issuer": "127.0.0.1",
                            "audience": ["127.0.0.1"],
                        }
                    }
                },
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
    def get_state(
        unit_of_work: UnitOfWorkInterface = Depends(get_unit_of_work),
        Repository: RepositoryInterface = Depends(get_repository),
        state_uuid: str = Depends(get_state_uuid),
        sign_state: bool = Depends(get_sign_state),
        secret_key: str = Depends(get_secret_key),
    ):
        """

        Use to get the application state using a session id.

        - **session_id (str)**: session id cookie.

        """

        state = services.get_state(
            unit_of_work, Repository, state_uuid, sign_state, secret_key
        )

        response = JSONResponse(state, status.HTTP_200_OK)

        return response
