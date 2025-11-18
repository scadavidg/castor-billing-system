"""
Authentication module for API token verification.
Validates API tokens from request headers to secure endpoints.
"""
import os
from fastapi import Header, HTTPException

def get_token_secret():
    """
    Get token secret from environment variable.
    Reads dynamically to support testing and runtime configuration.
    
    Returns:
        Token secret string from TOKEN_SECRET environment variable
    """
    return os.getenv("TOKEN_SECRET", "")

def verify_token(x_api_token: str = Header(None)):
    """
    Verify API token from request header.
    
    This dependency function validates the X-API-Token header value
    against the configured TOKEN_SECRET. Used as a FastAPI dependency
    to protect endpoints.
    
    Args:
        x_api_token: API token from X-API-Token request header
        
    Returns:
        True if token is valid
        
    Raises:
        HTTPException 401: If token is missing or invalid
    """
    # Get token secret dynamically (supports testing with different tokens)
    token_secret = get_token_secret()
    
    # Check if token header is present
    if x_api_token is None:
        raise HTTPException(status_code=401, detail="Token missing")

    # Validate token against secret
    if x_api_token != token_secret:
        raise HTTPException(status_code=401, detail="Invalid token")

    return True
