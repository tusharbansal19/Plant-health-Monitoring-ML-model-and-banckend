from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from schemas.user_schemas import (
    UserSignup, UserLogin, LoginResponse, RefreshTokenRequest, 
    TokenResponse, UserResponse, SignupResponse
)
from controllers.auth_controller import AuthController
from utils.auth_utils import decode_refresh_token, add_token_to_blacklist
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=SignupResponse)
def signup(user: UserSignup):
    """Register a new user with email validation and password strength requirements"""
    result = AuthController.signup(user.model_dump())
    return result


@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, response: Response):
    """Login with username/email and password. Returns access and refresh tokens."""
    login_result = AuthController.login(user.model_dump())
    
    # Set access token as httponly cookie
    response.set_cookie(
        key="access_token",
        value=login_result["access_token"],
        httponly=True,
        max_age=1800,  # 30 mins
        samesite="lax"
    )
    
    # Set refresh token as httponly cookie (optional, can also send in body)
    response.set_cookie(
        key="refresh_token",
        value=login_result["refresh_token"],
        httponly=True,
        max_age=604800,  # 7 days
        samesite="lax"
    )
    
    return login_result


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    result = AuthController.refresh_token(request.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    return result


@router.post("/logout")
def logout(response: Response, current_user: str = Depends(get_current_user)):
    """Logout by clearing cookies and blacklisting token"""
    # Get token from cookies or headers for blacklisting
    # This is a best-effort blacklist (for production use Redis)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logout successful"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: str = Depends(get_current_user)):
    """Get current logged-in user information"""
    result = AuthController.get_user_info(current_user)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return result
