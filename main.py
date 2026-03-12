from fastapi import FastAPI, Query, HTTPException
import requests
import pandas as pd

app = FastAPI(title="CryptoBot API")

BINANCE_URL = "https://api.binance.com/api/v3/klines"

AVAILABLE_CRYPTOS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "ADAUSDT",
    "XRPUSDT",
    "DOGEUSDT"
]

AVAILABLE_INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]
AVAILABLE_PERIODS = ["1D", "1W", "1M", "1Y"]


def period_to_limit(interval: str, period: str) -> int:
    mapping = {
        "1m": {"1D": 300, "1W": 1000, "1M": 1000, "1Y": 1000},
        "5m": {"1D": 288, "1W": 1000, "1M": 1000, "1Y": 1000},
        "15m": {"1D": 96, "1W": 672, "1M": 1000, "1Y": 1000},
        "1h": {"1D": 24, "1W": 168, "1M": 720, "1Y": 1000},
        "4h": {"1D": 6, "1W": 42, "1M": 180, "1Y": 1000},
        "1d": {"1D": 1, "1W": 7, "1M": 30, "1Y": 365},
    }
    return mapping[interval][period]


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

    if not isinstance(data, list) or len(data) == 0:
        raise HTTPException(status_code=500, detail="Aucune donnée reçue depuis Binance")

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["date"] = pd.to_datetime(df["open_time"], unit="ms")
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df[["date", "open", "high", "low", "close", "volume"]]


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    # EMA 20
    result["ema_20"] = result["close"].ewm(span=20, adjust=False).mean()

    # RSI 14
    delta = result["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)
    result["rsi"] = 100 - (100 / (1 + rs))
    result["rsi"] = result["rsi"].fillna(50)

    return result


def compute_signal(df: pd.DataFrame) -> dict:
    df = add_indicators(df)

    last_close = float(df["close"].iloc[-1])
    last_ema = float(df["ema_20"].iloc[-1])
    last_rsi = float(df["rsi"].iloc[-1])

    # Logique simple et débutante
    if last_close > last_ema and 50 <= last_rsi < 70:
        signal = "BUY"
        reason = "Prix au-dessus de l’EMA et RSI haussier sans surachat"
    elif last_close < last_ema and 30 < last_rsi < 50:
        signal = "SELL"
        reason = "Prix en-dessous de l’EMA et RSI baissier"
    else:
        signal = "HOLD"
        reason = "Conditions intermédiaires ou marché incertain"

    return {
        "signal": signal,
        "close": round(last_close, 2),
        "ema_20": round(last_ema, 2),
        "rsi": round(last_rsi, 2),
        "reason": reason
    }


@app.get("/")
def home():
    return {
        "message": "CryptoBot API running",
        "cryptos": AVAILABLE_CRYPTOS,
        "intervals": AVAILABLE_INTERVALS,
        "periods": AVAILABLE_PERIODS
    }


@app.get("/stats")
def stats(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = get_binance_data(symbol, interval, period)

    return {
        "symbol": symbol,
        "interval": interval,
        "period": period,
        "last_price": float(df["close"].iloc[-1]),
        "max_price": float(df["high"].max()),
        "min_price": float(df["low"].min()),
        "avg_volume": float(df["volume"].mean())
    }


@app.get("/charts")
def charts(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = get_binance_data(symbol, interval, period)
    df = add_indicators(df)

    df["date"] = df["date"].astype(str)

    return df.to_dict(orient="records")


@app.get("/signals")
def signals(
    symbol: str = Query("BTCUSDT"),
    interval: str = Query("1h"),
    period: str = Query("1D")
):
    df = get_binance_data(symbol, interval, period)
    return compute_signal(df)

    chart_df = df[["open_time", "close"]].copy()
    chart_df.columns = ["date", "close"]

    return chart_df.to_dict(orient="records")
