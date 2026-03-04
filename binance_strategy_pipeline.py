import requests
import pandas as pd


# 1 RÉCUPÉRATION API BINANCE


url = "https://api.binance.com/api/v3/klines"

params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 1000
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

data = response.json()

# 2 TRANSFORMATION DATAFRAME

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

df = pd.DataFrame(data, columns=columns)

# Conversion types numériques
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

# Conversion timestamp
df["date"] = pd.to_datetime(df["open_time"], unit="ms")

# Trier chronologiquement
df = df.sort_values("date")


# 3 STRATÉGIE (5 JOURS)


# 5 jours = 5 × 24 heures
horizon = 120
threshold = 0.02

df["future_return"] = (df["close"].shift(-horizon) - df["close"]) / df["close"]

# Création labels
labels = []

for value in df["future_return"]:
    if value > threshold:
        labels.append("Acheter")
    elif value < -threshold:
        labels.append("Vendre")
    else:
        labels.append("Attendre")

df["label"] = labels

# Supprimer NaN
df = df.dropna()

# 4 NETTOYAGE FINAL


df = df[["date", "open", "high", "low", "close", "volume", "future_return", "label"]]


# 5 SAUVEGARDE


df.to_csv("dataset_with_labels.csv", index=False)

print("Dataset créé avec succès")
print("Nombre de lignes :", len(df))
print("Distribution des classes :")
print(df["label"].value_counts())
print(df.head())
print(df.isnull().sum())