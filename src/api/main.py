from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.database import Database

from .resources import state_router


def create_api(
    api_key: str,
    database: Database,
    session_cookie_name: str = None,
    sign_state: bool = False,
    secret_key: Optional[str] = None,
    cors_allowed_origins: List[str] = ["*"],
    debug: bool = False,
    title: str = "State Manager",
    description: str = "",
    version: str = "0.1.0",
    contact: Optional[Dict[str, Union[str, Any]]] = None,
    terms_of_service: Optional[str] = None,
    license_info: Optional[Dict[str, Union[str, Any]]] = None,
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
    root_path: str = "",
    root_path_in_servers: bool = True,
    deprecated: Optional[bool] = None,
    docs_url: Optional[str] = "/docs",
    redoc_url: Optional[str] = "/redoc",
) -> FastAPI:

    if sign_state and not secret_key:
        raise Exception("To use sign states you need to set a secret_key")

    api = FastAPI(
        debug=debug,
        title=title,
        description=description,
        version=version,
        contact=contact,
        terms_of_service=terms_of_service,
        license_info=license_info,
        servers=servers,
        root_path=root_path,
        root_path_in_servers=root_path_in_servers,
        deprecated=deprecated,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    @api.on_event("shutdown")
    def shutdown():
        database.disconnect()

    api.add_api_route("/", lambda: RedirectResponse("/docs"),
                      include_in_schema=False)

    api.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @api.middleware("http")
    async def request_state_setter_middleware(request: Request, call_next):
        request.state.DATABASE = database
        request.state.SECRET_KEY = secret_key
        request.state.SESSION_COOKIE_NAME = session_cookie_name
        request.state.SIGN_STATE = sign_state
        request.state.API_KEY = api_key
        response = await call_next(request)
        return response

    api.include_router(state_router)

    return api
