from fastapi import APIRouter, HTTPException
from app.schemas.ml import (
    TrainingData, PredictionRequest, PredictionResponse, 
    ModelInfo, TrainingResponse
)
from app.ml.model_service import ml_service

router = APIRouter()

@router.post("/train", response_model=TrainingResponse)
def train_model(data: TrainingData):
    try:
        metrics = ml_service.train_model(data.X, data.y)
        return TrainingResponse(
            message="Model trained successfully",
            metrics=metrics
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        prediction = ml_service.predict(request.features)
        return PredictionResponse(prediction=prediction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-info", response_model=ModelInfo)
def get_model_info():
    info = ml_service.get_model_info()
    return ModelInfo(**info)

@router.get("/sample-data")
def get_sample_data():
    return ml_service.generate_sample_data()