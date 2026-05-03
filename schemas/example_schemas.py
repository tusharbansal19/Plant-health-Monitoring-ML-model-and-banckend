from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# ============================================================================
# Plant Prediction Schema
# ============================================================================

class PredictRequest(BaseModel):
    """Schema for plant health prediction input"""
    Soil_Moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage (0-100)")
    Ambient_Temperature: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    Humidity: float = Field(..., ge=0, le=100, description="Humidity percentage (0-100)")

    class Config:
        json_schema_extra = {
            "example": {
                "Soil_Moisture": 45.0,
                "Ambient_Temperature": 22.5,
                "Humidity": 65.0
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    prediction: str = Field(..., description="Predicted plant health status")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "healthy",
                "confidence": 0.9542
            }
        }


class HealthCheckResponse(BaseModel):
    """Schema for health check response"""
    status: str = Field(..., description="API status")
    classes: list[str] = Field(..., description="Available prediction classes")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "classes": ["healthy", "warning", "critical"]
            }
        }


# ============================================================================
# EXAMPLE: How to create a simple schema for plant health data
# ============================================================================

class PlantHealthInput(BaseModel):
    """Schema for plant health monitoring input"""
    plant_id: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Humidity percentage")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    ph_level: Optional[float] = Field(None, ge=0, le=14, description="Soil pH level")
    light_level: Optional[int] = Field(None, ge=0, description="Light level in lux")

    class Config:
        json_schema_extra = {
            "example": {
                "plant_id": "plant_001",
                "temperature": 22.5,
                "humidity": 65,
                "soil_moisture": 45.0,
                "ph_level": 6.5,
                "light_level": 5000
            }
        }


class PlantHealthResponse(BaseModel):
    """Schema for plant health monitoring response"""
    plant_id: str
    status: str  # "healthy", "warning", "critical"
    message: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "plant_id": "plant_001",
                "status": "healthy",
                "message": "All parameters within normal range",
                "timestamp": "2026-05-03T10:30:00"
            }
        }


# ============================================================================
# EXAMPLE: How to create a schema with custom validation
# ============================================================================

class PredictionInputAdvanced(BaseModel):
    """Schema for plant health prediction with custom validation"""
    features: list[float] = Field(..., min_length=1, max_length=10)
    model_version: str = Field(default="v1")

    @field_validator('features')
    @classmethod
    def validate_features(cls, v: list[float]) -> list[float]:
        """Ensure all features are valid numbers"""
        for i, feature in enumerate(v):
            if not isinstance(feature, (int, float)):
                raise ValueError(f'Feature {i} must be a number')
            if feature < 0 or feature > 100:
                raise ValueError(f'Feature {i} must be between 0 and 100')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "features": [22.5, 65, 45.0, 6.5, 5000],
                "model_version": "v1"
            }
        }


# ============================================================================
# UNCOMMENT AND EXTEND BELOW AS NEEDED FOR YOUR MODELS
# ============================================================================

# class YourModelHere(BaseModel):
#     """Your schema description"""
#     field_name: str = Field(..., description="Field description")
#     
#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "field_name": "example_value"
#             }
#         }

