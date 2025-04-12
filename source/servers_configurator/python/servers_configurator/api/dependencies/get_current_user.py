from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from servers_configurator.config import Config
from servers_configurator.api.utils.token_processor import TokenProcessor


bearer_scheme = APIKeyHeader(name="Authorization", description="Bearer token")

async def get_current_user(
    request: Request,
    token: str = Depends(bearer_scheme),
) -> str:
    config: Config = request.app.state.config
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    
    token = token.replace("Bearer ", "")
    return TokenProcessor.verify(token, config.servers_configurator_config.jwt_secret_key)
