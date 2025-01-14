from fastapi import HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED
from loguru import logger
from .config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Validate API key from Authorization header in Bearer format."""
    logger.debug(f"Validating API key. Required: {settings.require_api_key}")
    logger.debug(f"Received header: {api_key_header}")
    
    if not settings.require_api_key:
        # Skip validation completely if API key is not required
        return "not_required"
        
    # Only check API key if it's required
    if not api_key_header:
        logger.warning("No API key provided")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, 
            detail="Could not validate API key"
        )
    
    # OpenAI client sends the key in format "Bearer sk_..."
    try:
        # Handle case where Swagger UI might add "Bearer " prefix
        if api_key_header.startswith("Bearer "):
            api_key = api_key_header[7:]  # Remove "Bearer " prefix
        else:
            api_key = api_key_header
            
        logger.debug(f"Extracted API key: {api_key[:5]}...")
        
        if api_key != settings.api_key:
            logger.warning("Invalid API key provided")
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, 
                detail="Invalid API key"
            )
        
        return api_key
        
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

# Create a reusable dependency
require_api_key = Depends(verify_api_key) 