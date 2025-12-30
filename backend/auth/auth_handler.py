from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from auth.dependencies import security
from auth.auth_utils import decode_token

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract the current user's email from the JWT token.
    Returns the email string, not the full payload.
    """
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Extract the email from the 'sub' field in the JWT payload
    return payload.get("sub")  # Returns the email string

