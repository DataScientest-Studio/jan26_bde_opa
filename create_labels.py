import pandas as pd
import json

#  Liste de tes fichiers Binance
files = [
    "data/BTCUSDT_20260217_115915.json",
    "data/BTCUSDT_20260217_120430.json",
    "data/BTCUSDT_20260217_120546.json"
]

all_data = []

# 1️ Charger tous les fichiers
for file in files:
    with open(file, "r") as f:
        data = json.load(f)
        all_data.extend(data)  # on ajoute les lignes

# 2️Définir les colonnes Binance 
columns = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore"
]

df = pd.DataFrame(all_data, columns=columns)

# 3️ Conversion des types
df["close"] = df["close"].astype(float)
df["open_time"] = df["open_time"].astype(int)

# 4️ Convertir timestamp en date lisible
df["date"] = pd.to_datetime(df["open_time"], unit="ms")

# 5️ Trier par date
df = df.sort_values("date")

# 6️ Supprimer doublons si nécessaire
df = df.drop_duplicates(subset="open_time")

# 7️ Calcul du rendement futur
horizon = 120  # 5 jours (1h × 24 × 5) 
df["future_return"] = (df["close"].shift(-horizon) - df["close"]) / df["close"]

# 8️ Définir le seuil
threshold = 0.02  # 2%

# 9️ Création des labels
labels = []

for value in df["future_return"]:
    if value > threshold:
        labels.append("Acheter")
    elif value < -threshold:
        labels.append("Vendre")
    else:
        labels.append("Attendre")

df["label"] = labels

# 10 Supprimer NaN (fin du dataset)
df = df.dropna()

# 11  Sauvegarder
df.to_csv("dataset_with_labels.csv", index=False)

print("Dataset final créé.")
print("Distribution des classes :")
print(df["label"].value_counts())