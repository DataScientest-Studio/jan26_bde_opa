from fastapi import FastAPI
import requests
import pandas as pd

app = FastAPI()

BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
LIMIT = 100


@app.get("/")
def home():
    return {"test": "ok"}


def get_binance_data():
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT
    }
    response = requests.get(BINANCE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return df


@app.get("/stats")
def stats():
    df = get_binance_data()

    return {
        "last_price": float(df["close"].iloc[-1]),
        "max_price": float(df["high"].max()),
        "min_price": float(df["low"].min()),
        "average_volume": float(df["volume"].mean())
    }


@app.get("/charts")
def charts():
    df = get_binance_data()

    chart_df = df[["open_time", "close"]].copy()
    chart_df.columns = ["date", "close"]

    return chart_df.to_dict(orient="records")