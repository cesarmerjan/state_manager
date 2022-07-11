from fastapi import APIRouter, Depends

from src.api.resources.authentication.security import api_key_security

from .delete import register_delete_state_resource
from .get import register_get_state_resource
from .post import register_post_state_resource
from .status import register_state_status_resource

state_router = APIRouter(
    prefix="/state", tags=["state"], dependencies=[Depends(api_key_security)]
)

register_get_state_resource(state_router)
register_post_state_resource(state_router)
register_delete_state_resource(state_router)
register_state_status_resource(state_router)
