import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, List, Optional
import joblib
import os
from app.core.config import settings

class MLModelService:
    def __init__(self):
        self.model: Optional[LinearRegression] = None
        self.metrics: Dict[str, float] = {}
        self.is_trained = False
        
    def train_model(self, X: List[List[float]], y: List[float]) -> Dict[str, float]:
        X_array = np.array(X)
        y_array = np.array(y)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_array, y_array, test_size=0.2, random_state=42
        )
        
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.metrics = {"mse": mse, "r2_score": r2}
        self.is_trained = True
        
        # Save model
        self._save_model()
        
        return self.metrics
    
    def predict(self, features: List[float]) -> float:
        if not self.is_trained or self.model is None:
            raise ValueError("Model not trained yet")
        
        features_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features_array)
        return float(prediction[0])
    
    def get_model_info(self) -> Dict:
        return {
            "trained": self.is_trained,
            "model_type": "Linear Regression" if self.model else None,
            "metrics": self.metrics if self.is_trained else {}
        }
    
    def generate_sample_data(self) -> Dict:
        np.random.seed(42)
        X = np.random.randn(100, 3)
        y = 2 * X[:, 0] + 3 * X[:, 1] - X[:, 2] + np.random.randn(100) * 0.1
        
        return {
            "X": X.tolist(),
            "y": y.tolist(),
            "description": "Sample data: y = 2*x1 + 3*x2 - x3 + noise"
        }
    
    def _save_model(self):
        os.makedirs(settings.MODEL_PATH, exist_ok=True)
        model_path = os.path.join(settings.MODEL_PATH, "linear_model.joblib")
        joblib.dump(self.model, model_path)
    
    def load_model(self):
        model_path = os.path.join(settings.MODEL_PATH, "linear_model.joblib")
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            self.is_trained = True

# Global instance
ml_service = MLModelService()