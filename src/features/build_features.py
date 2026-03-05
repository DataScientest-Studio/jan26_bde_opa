import requests
import pandas as pd

#  Récupérer les données Binance
url = "https://api.binance.com/api/v3/klines"
params = {"symbol": "BTCUSDT", "interval": "1h", "limit": 1000}

response = requests.get(url, params=params, timeout=10)
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

data = response.json()

#  Transformer en DataFrame
columns = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
]

df = pd.DataFrame(data, columns=columns)

#  Nettoyer
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
df = df.drop(columns=["ignore"])

for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

df["date"] = df["open_time"]
df = df.sort_values("date")

# Créer les labels (5 jours = 120 heures)
horizon = 120
threshold = 0.02

df["future_return"] = (df["close"].shift(-horizon) - df["close"]) / df["close"]

labels = []
for value in df["future_return"]:
    if value > threshold:
        labels.append("Acheter")
    elif value < -threshold:
        labels.append("Vendre")
    else:
        labels.append("Attendre")

df["label"] = labels
df = df.dropna()

#  Garder colonnes utiles
df = df[["date", "open", "high", "low", "close", "volume", "future_return", "label"]]

# Sauvegarder
df.to_csv("src/data/dataset_with_labels.csv", index=False)

print("✅ Dataset créé avec succès")
print("Nombre de lignes :", len(df))
print(df["label"].value_counts())
print(df.head())