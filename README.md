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



# Deployment on Render  

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
