import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

# 1) Charger le dataset
DATA_PATH = Path("src/data/dataset_with_labels.csv")
df = pd.read_csv(DATA_PATH)

# 2) Préparer X (features) et y (label)
X = df[["open", "high", "low", "close", "volume", "future_return"]]
y = df["label"]  # "Acheter" / "Vendre" / "Attendre"

# 3) Split train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4) Modèle simple
model = RandomForestClassifier(random_state=42, n_estimators=200)
model.fit(X_train, y_train)

# 5) Évaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("✅ Modèle entraîné")
print("Accuracy:", acc)
print(classification_report(y_test, y_pred))

# 6) Sauvegarde du modèle
OUT_DIR = Path("models")
OUT_DIR.mkdir(exist_ok=True)

MODEL_PATH = OUT_DIR / "model.pkl"
joblib.dump(model, MODEL_PATH)

print(f"✅ Modèle sauvegardé: {MODEL_PATH}")