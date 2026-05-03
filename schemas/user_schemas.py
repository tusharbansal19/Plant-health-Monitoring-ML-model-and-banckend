from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserSignup(BaseModel):
    """Schema for user registration/signup"""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be 3-50 characters")
    email: EmailStr = Field(..., description="Valid email address required")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format - alphanumeric and underscore only"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    identifier: str = Field(..., min_length=1, description="Username or email address")
    password: str = Field(..., min_length=1, description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "identifier": "john_doe",
                "password": "SecurePass123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    username: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str = Field(..., description="JWT access token (valid for 30 minutes)")
    refresh_token: str = Field(..., description="JWT refresh token (valid for 7 days)")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiry in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class LoginResponse(BaseModel):
    """Schema for complete login response"""
    message: str
    user: UserResponse
    token: TokenResponse

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Login successful",
                "user": {
                    "username": "john_doe",
                    "email": "john@example.com"
                },
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        }


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str = Field(..., description="Valid refresh token")

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class SignupResponse(BaseModel):
    """Schema for signup response"""
    message: str
    username: str
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "User created successfully",
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
