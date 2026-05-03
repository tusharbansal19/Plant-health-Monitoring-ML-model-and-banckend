from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from utils.auth_utils import decode_access_token, is_token_blacklisted
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

async def get_current_user(request: Request, token: Optional[str] = Depends(oauth2_scheme)):
    # Try to get token from cookie first
    cookie_token = request.cookies.get("access_token")
    
    # Use cookie token if available, otherwise fallback to header token
    final_token = cookie_token or token

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not final_token:
        raise credentials_exception

    # Check if token is blacklisted (logged out)
    if is_token_blacklisted(final_token):
        raise credentials_exception

    payload = decode_access_token(final_token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    return username

