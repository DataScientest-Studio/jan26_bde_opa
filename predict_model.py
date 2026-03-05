from pathlib import Path
import joblib
import pandas as pd


def load_model():
    # racine du projet
    project_root = Path(__file__).resolve().parent

    model_path = project_root / "models" / "model.pkl"

    return joblib.load(model_path)


def predict_one(model, features: dict) -> dict:
    X = pd.DataFrame([features])
    pred = int(model.predict(X)[0])

    return {
        "prediction": pred,
        "signal": "UP" if pred == 1 else "DOWN"
    }


# test du modèle
if __name__ == "__main__":

    features = {
        "open": 50000,
        "high": 50500,
        "low": 49500,
        "close": 50200,
        "volume": 1200
    }

    model = load_model()

    result = predict_one(model, features)

    print(result)





