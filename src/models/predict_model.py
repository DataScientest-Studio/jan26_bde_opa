from pathlib import Path
import joblib
import pandas as pd


def load_model():
    """
    Charge le modèle depuis models/model.pkl (racine projet).
    """
    project_root = Path(__file__).resolve().parents[2]
    model_path = project_root / "models" / "model.pkl"
    return joblib.load(model_path)


def predict_one(model, features: dict) -> dict:
    """
    features attendu: open, high, low, close, volume
    """
    X = pd.DataFrame([features])
    pred = int(model.predict(X)[0])
    return {"prediction": pred, "signal": "UP" if pred == 1 else "DOWN"}