from pydantic import BaseModel
from typing import List, Dict, Any

class TrainingData(BaseModel):
    X: List[List[float]]
    y: List[float]

class PredictionRequest(BaseModel):
    features: List[float]

class PredictionResponse(BaseModel):
    prediction: float

class ModelInfo(BaseModel):
    trained: bool
    model_type: str
    metrics: Dict[str, Any]

class TrainingResponse(BaseModel):
    message: str
    metrics: Dict[str, float]