import json
import os
from fastapi import HTTPException, status
from utils.auth_utils import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, decode_refresh_token
)

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

class AuthController:
    @staticmethod
    def signup(user_data: dict):
        users = load_users()
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")

        if username in users:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        for user in users.values():
            if user.get("email") == email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        hashed_password = get_password_hash(password)
        users[username] = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        save_users(users)
        return {
            "message": "User created successfully",
            "username": username,
            "email": email
        }

    @staticmethod
    def login(login_data: dict):
        users = load_users()
        identifier = login_data.get("identifier")  # This can be username or email
        password = login_data.get("password")

        user = None
        username = None
        
        # Try finding by username
        if identifier in users:
            user = users[identifier]
            username = identifier
        else:
            # Try finding by email
            for u_name, u_data in users.items():
                if u_data.get("email") == identifier:
                    user = u_data
                    username = u_name
                    break

        if not user or not verify_password(password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create both access and refresh tokens
        access_token = create_access_token(data={"sub": username, "email": user.get("email")})
        refresh_token = create_refresh_token(data={"sub": username})
        
        return {
            "message": "Login successful",
            "user": {
                "username": username,
                "email": user.get("email")
            },
            "token": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 1800  # 30 minutes in seconds
            }
        }

    @staticmethod
    def refresh_token(refresh_token: str):
        """Create new access token from refresh token"""
        payload = decode_refresh_token(refresh_token)
        if not payload:
            return None
        
        username = payload.get("sub")
        users = load_users()
        
        if username not in users:
            return None
        
        user = users[username]
        new_access_token = create_access_token(data={"sub": username, "email": user.get("email")})
        
        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,  # Return same refresh token (can extend if needed)
            "token_type": "bearer",
            "expires_in": 1800
        }

    @staticmethod
    def get_user_info(username: str):
        """Get user information"""
        users = load_users()
        if username not in users:
            return None
        
        user = users[username]
        return {
            "username": username,
            "email": user.get("email")
        }

