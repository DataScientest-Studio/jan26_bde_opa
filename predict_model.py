from pathlib import Path
import joblib
import pandas as pd


def load_model():
    project_root = Path(__file__).resolve().parent
    model_path = project_root / "models" / "model.pkl"
    return joblib.load(model_path)


def predict_one(model, features: list[dict]) -> dict:
    X = pd.DataFrame(features)
    pred = int(model.predict(X)[0])

    return {
        "prediction": pred,
        "signal": "UP" if pred == 1 else "DOWN"
    }




