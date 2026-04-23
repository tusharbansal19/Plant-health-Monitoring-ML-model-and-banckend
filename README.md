# 🌿 Plant Health Monitoring — ML Backend

A production-ready REST and WebSocket API for predicting plant health status using a trained Random Forest classifier. Built with FastAPI and deployed on Render.

---

## 🚀 Live Deployment

| Resource | URL |
|---|---|
| **Base URL** | https://plant-health-monitor-banckend.onrender.com |
| **Swagger UI** | https://plant-health-monitor-banckend.onrender.com/docs |
| **Health Check** | https://plant-health-monitor-banckend.onrender.com/health |
| **WebSocket** | wss://plant-health-monitor-banckend.onrender.com/ws |

---

## 📋 Project Overview

This system monitors plant health in real time by analysing environmental sensor readings. A Random Forest model trained on 1,200 timestamped plant observations predicts one of three health states:

- **Healthy**
- **Moderate Stress**
- **High Stress**

**Model accuracy: 91.25%** (test set, 240 samples)

---

## 📊 Model Details

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier |
| Features | `Soil_Moisture`, `Ambient_Temperature`, `Humidity` |
| Target | `Plant_Health_Status` |
| Estimators | 300 |
| Max depth | 15 |
| Test accuracy | **91.25%** |
| Top feature | `Soil_Moisture` (~79% importance) |

---

## 🔌 API Reference

### `POST /predict`

Predict plant health from sensor readings.

**Request**
```json
{
  "Soil_Moisture": 45.0,
  "Ambient_Temperature": 25.0,
  "Humidity": 60.0
}
```

**Response**
```json
{
  "prediction": "Healthy",
  "confidence": 0.8600
}
```

---

### `GET /health`

Returns API and model status.

**Response**
```json
{
  "status": "ok",
  "classes": ["Healthy", "High Stress", "Moderate Stress"]
}
```

---

### `WS /ws`

Real-time WebSocket predictions. Send JSON, receive prediction instantly.

**Send**
```json
{"Soil_Moisture": 12.0, "Ambient_Temperature": 35.0, "Humidity": 20.0}
```

**Receive**
```json
{"prediction": "High Stress", "confidence": 0.8181}
```

**Test locally:**
```bash
python test_websocket.py
```

---

## 🗂️ Project Structure

```
├── train.py                  # Model training script
├── main.py                   # FastAPI application
├── test_websocket.py         # WebSocket test client
├── DataEngineering.ipynb     # Full data engineering pipeline
├── model.pkl                 # Trained Random Forest model
├── label_encoder.pkl         # Label encoder for target classes
├── plant_health_cleaned.csv  # Cleaned dataset (pipeline output)
├── requirements.txt          # Python dependencies
├── render.yaml               # Render deployment config
└── .env                      # Environment variables (not committed)
```

---

## ⚙️ Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python train.py

# Start the API server
python -m uvicorn main:app --host 0.0.0.0 --port 10000

# Test WebSocket
python test_websocket.py
```

Swagger UI available at: `http://localhost:10000/docs`

---

## ☁️ Deployment (Render)

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python -m uvicorn main:app --host 0.0.0.0 --port 10000` |
| Environment Variables | `MODEL_PATH`, `ENCODER_PATH` |

---

## 🛠️ Tech Stack

- **Python 3.12**
- **FastAPI** — REST + WebSocket API
- **scikit-learn** — Random Forest model
- **pandas / numpy** — Data processing
- **Render** — Cloud deployment
