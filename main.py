import json
import os
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_routes
from middleware.auth_middleware import get_current_user
from fastapi import Depends
from schemas.example_schemas import PredictRequest

load_dotenv()

model = joblib.load(os.getenv("MODEL_PATH", "model.pkl"))
le = joblib.load(os.getenv("ENCODER_PATH", "label_encoder.pkl"))

FEATURES = ["Soil_Moisture", "Ambient_Temperature", "Humidity"]

app = FastAPI(
    title="Plant Health Prediction API",
    description="Predict plant health status using ML model with JWT authentication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)

# Start background keep-alive pinger if available
try:
    from keep_alive import start_keep_alive
    @app.on_event("startup")
    def _start_keep_alive():
        start_keep_alive()
except Exception:
    pass

# Connected WebSocket clients
clients = set()


def predict(data: dict):
    feature_values = [data[f] for f in FEATURES]
    X = pd.DataFrame([feature_values], columns=FEATURES)
    pred = model.predict(X)[0]
    confidence = float(np.max(model.predict_proba(X)[0]))
    label = le.inverse_transform([pred])[0]
    return label, confidence


@app.get("/health")
def health():
    return {"status": "ok", "classes": list(le.classes_)}


@app.post("/predict")
def predict_endpoint(request: PredictRequest, current_user: str = Depends(get_current_user)):
    try:
        label, confidence = predict(request.model_dump())
        return {"prediction": label, "confidence": round(confidence, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            try:
                raw = await websocket.receive_text()
                data = json.loads(raw)

                missing = [f for f in FEATURES if f not in data]
                if missing:
                    await websocket.send_text(json.dumps({"error": f"Missing fields: {missing}"}))
                    continue

                label, confidence = predict(data)
                response = json.dumps({
                    "input": data,
                    "prediction": label,
                    "confidence": round(confidence, 4)
                })

                for client in clients:
                    try:
                        await client.send_text(response)
                    except:
                        pass

            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))

    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)

@app.websocket("/ws1")
async def websocket_endpoint_1(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
                missing = [f for f in FEATURES if f not in data]
                if missing:
                    await websocket.send_text(json.dumps({"error": f"Missing fields: {missing}"}))
                    continue
                label, confidence = predict(data)
                await websocket.send_text(json.dumps({"prediction": label, "confidence": round(confidence, 4)}))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
    except WebSocketDisconnect:
        pass