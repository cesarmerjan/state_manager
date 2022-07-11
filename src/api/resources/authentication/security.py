from fastapi import Depends, Security, status
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException

from src.api.resources.dependencies import get_api_key

API_KEY_NAME = "Authorization"


api_key_header = APIKeyHeader(
    name=API_KEY_NAME, scheme_name="API key header", auto_error=False
)


async def api_key_security(
    header_param: str = Security(api_key_header), API_KEY: str = Depends(get_api_key)
):

    if not header_param:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Missing API Key"
        )

    elif header_param == API_KEY:
        return header_param

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong, revoked, or expired API key.",
        )
