# Render Deployment Guide

## Environment Variables to Set on Render

Set these in your Render dashboard under **Environment**:

```
SECRET_KEY=94b7c84594c7b8e1f5d6a2c3b4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3
MODEL_PATH=model.pkl
ENCODER_PATH=label_encoder.pkl
HOST=0.0.0.0
PORT=10000
```

## Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

## Important Files to Include

Make sure these files are committed to Git:
- ✅ `model.pkl` - Trained ML model
- ✅ `label_encoder.pkl` - Label encoder
- ✅ All Python files
- ✅ `.env.example` (no secrets!)

## .gitignore Setup

Add to `.gitignore`:
```
.env
users.json
__pycache__/
*.pyc
.DS_Store
node_modules/
dist/
.venv/
```

## API Endpoints on Render

Once deployed, your API will be at:
```
https://your-app-name.onrender.com
```

**Available Routes:**
- `POST /auth/signup` - Register
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get current user
- `POST /auth/logout` - Logout
- `GET /health` - Health check
- `POST /predict` - Make prediction (requires auth)
- `WS /ws` - WebSocket broadcast
- `WS /ws1` - WebSocket individual
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Frontend WebSocket Update

Update your React WebSocket URL:

**Local Development:**
```javascript
const socket = new WebSocket("ws://127.0.0.1:8001/ws");
```

**Production on Render:**
```javascript
const socket = new WebSocket("wss://your-app-name.onrender.com/ws");
```

Note: Change `ws://` to `wss://` for secure WebSocket on HTTPS.

## Create .env.example

Create a `.env.example` file with template values:

```
SECRET_KEY=your-secret-key-here
MODEL_PATH=model.pkl
ENCODER_PATH=label_encoder.pkl
HOST=0.0.0.0
PORT=10000
```

## Troubleshooting

### 500 Internal Server Error on Login
- ✅ Check all environment variables are set
- ✅ Ensure `model.pkl` and `label_encoder.pkl` are included
- ✅ Check Render logs for detailed errors

### WebSocket Connection Failed
- ✅ Update URL to use `wss://` (secure WebSocket)
- ✅ Ensure CORS is properly configured
- ✅ Check that your app is running

### Users File Permission Error
- ✅ The app now uses proper file paths
- ✅ `users.json` is created in the project root
- ✅ No manual action needed

## Deployment Steps on Render

1. Push code to GitHub
2. Go to https://render.com
3. Create new Web Service
4. Connect GitHub repository
5. Set:
   - **Name**: your-app-name
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Environment**: Add all vars from above
6. Click Deploy
7. Wait for build to complete
8. Test at `https://your-app-name.onrender.com/docs`

## Testing Deployment

```bash
# Test health endpoint
curl https://your-app-name.onrender.com/health

# Test signup
curl -X POST https://your-app-name.onrender.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"TestPass123"}'

# Test login
curl -X POST https://your-app-name.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"test","password":"TestPass123"}'
```

## Production Best Practices

1. **Use a Database** - Replace `users.json` with PostgreSQL or MongoDB
2. **Redis Cache** - Use Redis instead of in-memory token blacklist
3. **Environment Secrets** - Use Render's built-in secrets manager
4. **HTTPS/WSS** - Render automatically provides HTTPS
5. **Rate Limiting** - Add rate limiting to auth endpoints
6. **Monitoring** - Set up error tracking with Sentry
7. **Backups** - Backup user data regularly
