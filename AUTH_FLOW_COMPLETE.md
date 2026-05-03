# Complete Authentication & Token Flow Documentation

## Overview
This is a complete JWT-based authentication system with access tokens, refresh tokens, and secure logout.

---

## API Endpoints

### 1. **Sign Up** - Register New User
```http
POST /auth/signup
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

### 2. **Login** - Get Access & Refresh Tokens
```http
POST /auth/login
Content-Type: application/json

{
  "identifier": "john_doe",  // or email
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "username": "john_doe",
    "email": "john@example.com"
  },
  "token": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImVtYWlsIjoiam9obkBleGFtcGxlLmNvbSIsImV4cCI6MTcxNDc1OTQwMH0...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTcxNTM2NDIwMH0...",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

**Cookies Set:**
- `access_token` (httpOnly, 30 min)
- `refresh_token` (httpOnly, 7 days)

---

### 3. **Get Current User** - Retrieve User Info
```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

### 4. **Refresh Token** - Get New Access Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### 5. **Logout** - Clear Session
```http
POST /auth/logout
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## Token Flow Diagram

```
User Login
    ↓
[Verify Credentials]
    ↓
Create Access Token (30 min) + Refresh Token (7 days)
    ↓
Set as HTTPOnly Cookies + Return in Response Body
    ↓
┌─────────────────────────────────────┐
│  Access Token Expires (30 min)      │
│  Use Refresh Endpoint to Get New    │
│  Access Token                       │
└─────────────────────────────────────┘
    ↓
[Optional] Logout → Clear Cookies + Blacklist Tokens
```

---

## Protected Endpoints

### Using Access Token
```http
POST /predict
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "Soil_Moisture": 45.5,
  "Ambient_Temperature": 22.3,
  "Humidity": 65.0
}
```

The middleware automatically extracts the token from:
1. **Cookie** (`access_token`) - Priority 1
2. **Header** (`Authorization: Bearer <token>`) - Priority 2

---

## Client Implementation Examples

### JavaScript/Fetch
```javascript
// Login
const loginRes = await fetch('/auth/login', {
  method: 'POST',
  credentials: 'include',  // Include cookies
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ identifier: 'john_doe', password: 'SecurePass123' })
});
const data = await loginRes.json();
const accessToken = data.token.access_token;
const refreshToken = data.token.refresh_token;

// Use access token
const predictRes = await fetch('/predict', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ Soil_Moisture: 45, Ambient_Temperature: 22, Humidity: 65 })
});

// Refresh when expired
const refreshRes = await fetch('/auth/refresh', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refresh_token: refreshToken })
});
const newTokens = await refreshRes.json();
```

### Python/Requests
```python
import requests

# Login
login_res = requests.post(
    'http://localhost:10000/auth/login',
    json={'identifier': 'john_doe', 'password': 'SecurePass123'}
)
tokens = login_res.json()['token']
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

# Use access token
predict_res = requests.post(
    'http://localhost:10000/predict',
    headers={'Authorization': f'Bearer {access_token}'},
    json={'Soil_Moisture': 45, 'Ambient_Temperature': 22, 'Humidity': 65}
)

# Refresh when needed
refresh_res = requests.post(
    'http://localhost:10000/auth/refresh',
    json={'refresh_token': refresh_token}
)
new_tokens = refresh_res.json()
```

---

## Token Validation Details

### Access Token Payload
```json
{
  "sub": "john_doe",
  "email": "john@example.com",
  "exp": 1714759400,
  "type": "access"
}
```

### Refresh Token Payload
```json
{
  "sub": "john_doe",
  "exp": 1715364200,
  "type": "refresh"
}
```

---

## Security Features

✅ **JWT Tokens** - Cryptographically signed claims  
✅ **HTTPOnly Cookies** - Protected from XSS attacks  
✅ **Refresh Tokens** - Separate long-lived tokens  
✅ **Token Type Validation** - Verify "access" vs "refresh"  
✅ **Expiration Checks** - Automatic JWT exp validation  
✅ **Blacklist Support** - Logout invalidation (in-memory, use Redis for production)  
✅ **Password Hashing** - bcrypt with auto-generated salt  
✅ **Pydantic Validation** - Input sanitization & email validation  

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 422 Unprocessable Entity (Validation Error)
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must contain at least one uppercase letter",
      "type": "value_error"
    }
  ]
}
```

### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

---

## Production Recommendations

1. **Use Redis for Token Blacklist** - In-memory set won't persist across restarts
2. **HTTPS Only** - Always use HTTPS in production
3. **Strict CORS** - Change `allow_origins=["*"]` to specific domains
4. **Environment Variables** - Keep SECRET_KEY in `.env` file
5. **Rate Limiting** - Add rate limiting to auth endpoints
6. **Token Rotation** - Optionally rotate refresh tokens on each refresh
7. **Database** - Use proper database instead of JSON file
8. **Audit Logs** - Log all auth events for security monitoring
