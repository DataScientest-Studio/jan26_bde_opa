import requests
import json
from datetime import datetime


class BinanceExtractor:

    BASE_URL = "https://api.binance.com/api/v3/klines"

    def __init__(self, symbol="BTCUSDT", interval="1h", limit=100):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

    def fetch_data(self):
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": self.limit
        }

        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            print("✅ Données récupérées avec succès")
            return response.json()
        else:
            print("❌ Erreur API :", response.status_code)
            return None

    def save_to_json(self, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/{self.symbol}_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(data, f)

        print(f"📁 Fichier sauvegardé : {filename}")


if __name__ == "__main__":
    extractor = BinanceExtractor(symbol="BTCUSDT", interval="1h", limit=50)
    data = extractor.fetch_data()

    if data:
        extractor.save_to_json(data)
import pandas as pd
import json


def load_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def preprocess_klines(data):
    df = pd.DataFrame(data, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","quote_asset_volume","nb_trades",
        "taker_buy_base","taker_buy_quote","ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

    numeric_cols = ["open","high","low","close","volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df


if __name__ == "__main__":
    filepath = "data/BTCUSDT_20260217_115915.json"  # adapte si besoin
    raw_data = load_json(filepath)
    df = preprocess_klines(raw_data)

    print(df.head())
