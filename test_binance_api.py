import requests
import pandas as pd

# 1 RÉCUPÉRER  API


url = "https://api.binance.com/api/v3/klines"

params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 1000
}

response = requests.get(url, params=params)
data = response.json()

# 2 TRANSFORMER  EN DATAFRAME


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

df["close"] = df["close"].astype(float)
df["date"] = pd.to_datetime(df["open_time"], unit="ms")
df = df.sort_values("date")


# 3 STRATÉGIE 5 JOURS


horizon = 120  # 5 jours (1h × 24 × 5)
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

# 4 SAUVEGARDE


df.to_csv("dataset_with_labels.csv", index=False)

print("Dataset créé avec succès")
print(df["label"].value_counts())