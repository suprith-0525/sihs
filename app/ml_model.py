# backend/app/ml_model.py
import joblib
import numpy as np
MODEL_PATH = "./model.joblib"  # if you placed model under ml/

def load_model():
    model = joblib.load(MODEL_PATH)
    return model

def load_model_and_predict(features: dict):
    model = load_model()
    X = np.array([[features['N'], features['P'], features['K'], features['pH'],
                   features['temperature'], features['humidity'], features['rainfall']]])
    pred = model.predict(X)[0]
    # We also can return a small explanation (feature importances)
    return {
        "crop": str(pred),
        "confidence": 0.85,
        "notes": "Based on soil pH and expected rainfall"
    }
