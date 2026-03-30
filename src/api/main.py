from fastapi import FastAPI, Query, HTTPException
import requests
import pandas as pd

app = FastAPI(title="CryptoBot API")

BINANCE_URL = "https://api.binance.com/api/v3/klines"

AVAILABLE_CRYPTOS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT",
    "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"
]

AVAILABLE_INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]
AVAILABLE_PERIODS = ["1D", "1W", "1M", "1Y"]


# Conversion période → nombre de points
def period_to_limit(interval: str, period: str) -> int:
    mapping = {
        "1m": {"1D": 300, "1W": 1000, "1M": 1000, "1Y": 1000},
        "5m": {"1D": 288, "1W": 1000, "1M": 1000, "1Y": 1000},
        "15m": {"1D": 96, "1W": 672, "1M": 1000, "1Y": 1000},
        "1h": {"1D": 24, "1W": 168, "1M": 720, "1Y": 1000},
        "4h": {"1D": 6, "1W": 42, "1M": 180, "1Y": 1000},
        "1d": {"1D": 1, "1W": 7, "1M": 30, "1Y": 365},
    }

    if interval not in mapping or period not in mapping[interval]:
        raise HTTPException(status_code=400, detail="Combinaison interval/période invalide")

    return mapping[interval][period]


# Récupération données Binance
def get_binance_data(symbol: str, interval: str, period: str) -> pd.DataFrame:
    if symbol not in AVAILABLE_CRYPTOS:
        raise HTTPException(status_code=400, detail="Crypto non supportée")
    if interval not in AVAILABLE_INTERVALS:
        raise HTTPException(status_code=400, detail="Intervalle non supporté")
    if period not in AVAILABLE_PERIODS:
        raise HTTPException(status_code=400, detail="Période non supportée")

    limit = period_to_limit(interval, period)

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(BINANCE_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise HTTPException(status_code=500, detail="Aucune donnée Binance")

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "trades", "tbav", "tqav", "ignore"
    ])

    df["date"] = pd.to_datetime(df["open_time"], unit="ms")

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df[["date", "open", "high", "low", "close", "volume"]]


# INDICATEURS (EMA + RSI) 
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # EMA 20
    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    # RSI 14
    delta = df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-10)

    df["rsi"] = 100 - (100 / (1 + rs))
    df["rsi"] = df["rsi"].fillna(50)

    return df



@app.get("/")
def home():
    return {"message": "CryptoBot API running"}


# STATS
@app.get("/stats")
def stats(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = get_binance_data(symbol, interval, period)

    return {
        "last_price": float(df["close"].iloc[-1]),
        "max_price": float(df["high"].max()),
        "min_price": float(df["low"].min()),
        "avg_volume": float(df["volume"].mean())
    }


# CHARTS
@app.get("/charts")
def charts(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = add_indicators(get_binance_data(symbol, interval, period))
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")


# SIGNAL
@app.get("/signals")
def signals(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = add_indicators(get_binance_data(symbol, interval, period))

    last_close = df["close"].iloc[-1]
    ema = df["ema_20"].iloc[-1]
    rsi = df["rsi"].iloc[-1]

    if last_close > ema and rsi > 50:
        signal = "BUY"
        reason = "Tendance haussière"
    elif last_close < ema and rsi < 50:
        signal = "SELL"
        reason = "Tendance baissière"
    else:
        signal = "HOLD"
        reason = "Marché neutre"

    return {
        "signal": signal,
        "close": round(last_close, 2),
        "ema_20": round(ema, 2),
        "rsi": round(rsi, 2),
        "reason": reason
    }
