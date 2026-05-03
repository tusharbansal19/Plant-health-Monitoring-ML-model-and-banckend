# Pydantic Input Validation Guide

## Overview
This project uses **Pydantic** for automatic input validation on all API endpoints. FastAPI integrates seamlessly with Pydantic to validate and document request data.

## Features Enabled
- ✅ Automatic validation of request bodies
- ✅ Type checking and conversion
- ✅ Email validation (EmailStr)
- ✅ Custom field validators
- ✅ Auto-generated OpenAPI documentation
- ✅ Clear error messages for invalid input

## How to Use

### 1. Basic Model with Type Hints
```python
from pydantic import BaseModel, Field

class PlantData(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    ph_level: float = Field(..., ge=0, le=14)  # Between 0 and 14
    humidity: int = Field(..., ge=0, le=100)   # Percentage
```

### 2. Email Validation
```python
from pydantic import EmailStr

class Contact(BaseModel):
    email: EmailStr  # Automatically validates email format
    username: str
```

### 3. Custom Validators
```python
from pydantic import BaseModel, field_validator
import re

class User(BaseModel):
    username: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric with underscores only')
        return v
```

### 4. Conditional Validation
```python
from pydantic import field_validator

class Plant(BaseModel):
    name: str
    plant_type: str
    
    @field_validator('plant_type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed_types = ['indoor', 'outdoor', 'aquatic']
        if v.lower() not in allowed_types:
            raise ValueError(f'Must be one of {allowed_types}')
        return v.lower()
```

### 5. Using in FastAPI Routes
```python
from fastapi import APIRouter
from schemas.user_schemas import UserSignup

router = APIRouter()

@router.post("/register")
def register(user: UserSignup):  # Validation happens automatically
    # If user data is invalid, FastAPI returns 422 with error details
    # If valid, user is a UserSignup instance with all data properly typed
    return {"message": f"User {user.username} registered"}
```

## Common Field Constraints

| Constraint | Usage | Example |
|-----------|-------|---------|
| Required | `Field(...)` | `name: str = Field(...)` |
| Min/Max Length | `min_length`, `max_length` | `Field(..., min_length=3, max_length=50)` |
| Min/Max Value | `ge`, `le` (for numbers) | `Field(..., ge=0, le=100)` |
| Pattern | Use `@field_validator` | See examples above |
| Email | `EmailStr` | `email: EmailStr` |
| Optional | `Optional[Type]` | `phone: Optional[str] = None` |
| Default Value | `Field(default=value)` | `status: str = Field(default="active")` |

## Error Response Example

**Invalid Request:**
```json
{
  "username": "a",
  "email": "invalid-email",
  "password": "weak"
}
```

**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "ensure this value has at least 3 characters",
      "type": "value_error.any_str.min_length"
    },
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    },
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

## Current Models

Located in `schemas/`:
- **user_schemas.py**: `UserSignup`, `UserLogin`, `UserResponse`, `LoginResponse`

## Adding New Models

1. Create a new file in `schemas/` (e.g., `schemas/plant_schemas.py`)
2. Define your Pydantic models with validation
3. Import and use in your routes

## FastAPI Auto Documentation

Once deployed, your API docs will be available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

All validation rules and examples will appear in the documentation automatically!
