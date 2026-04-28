import json
import os
import joblib
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

model = joblib.load(os.getenv("MODEL_PATH", "model.pkl"))
le = joblib.load(os.getenv("ENCODER_PATH", "label_encoder.pkl"))

FEATURES = ["Soil_Moisture", "Ambient_Temperature", "Humidity"]

app = FastAPI(title="Plant Health Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


clients = set()

class PredictRequest(BaseModel):
    Soil_Moisture: float
    Ambient_Temperature: float
    Humidity: float


def predict(data: dict):
    X = pd.DataFrame([[data[f] for f in FEATURES]], columns=FEATURES)
    pred = model.predict(X)[0]
    confidence = float(np.max(model.predict_proba(X)[0]))
    label = le.inverse_transform([pred])[0]
    return label, confidence


@app.get("/health")
def health():
    return {"status": "ok", "classes": list(le.classes_)}


@app.post("/predict")
def predict_endpoint(request: PredictRequest):
    try:
        label, confidence = predict(request.model_dump())
        return {"prediction": label, "confidence": round(confidence, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

           
            label, confidence = predict(data)
            print("label",label)
            print("confidence",confidence)
            print("data",data)

           
            response = json.dumps({
                "input": data,
                "prediction": label,
                "confidence": round(confidence, 4)
            })

          
            for client in clients:
                await client.send_text(response)

    except WebSocketDisconnect:
        clients.remove(websocket)
