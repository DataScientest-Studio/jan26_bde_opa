from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from src.storage.pg import get_pg_connection

app = FastAPI(title="CryptoBot API PG Ready")

AVAILABLE_CRYPTOS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"]
AVAILABLE_INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]
AVAILABLE_PERIODS = ["1D", "1W", "1M", "1Y"]

def period_to_limit(period: str) -> int:
    mapping = {"1D": 24, "1W": 168, "1M": 720, "1Y": 8760}
    return mapping.get(period, 24)

def fetch_dashboard(symbol: str, interval: str):
    """Récupère les données du dashboard depuis dashboard_metrics"""
    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT last_price, max_price, min_price, avg_volume, ema_20, rsi
        FROM dashboard_metrics
        WHERE symbol=%s AND interval=%s
    """, (symbol, interval))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Dashboard metrics non trouvées")
    keys = ["last_price", "max_price", "min_price", "avg_volume", "ema_20", "rsi"]
    return dict(zip(keys, row))

def fetch_ml_features(symbol: str, interval: str, period: str):
    """Récupère les données ML depuis ml_features"""
    conn = get_pg_connection()
    cursor = conn.cursor()
    limit = period_to_limit(period)
    cursor.execute("""
        SELECT open_time, close, return_1h, ma_24, volatility_24, ema_20, rsi
        FROM ml_features
        WHERE symbol=%s AND interval=%s
        ORDER BY open_time DESC
        LIMIT %s
    """, (symbol, interval, limit))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="ML features non trouvées")
    df = pd.DataFrame(rows, columns=["open_time", "close", "return_1h", "ma_24", "volatility_24", "ema_20", "rsi"])
    df = df.sort_values("open_time")
    df["date"] = pd.to_datetime(df["open_time"])
    return df

def fetch_candles(symbol: str, interval: str, period: str):
    """Récupère l’historique complet depuis candles (graphique)"""
    conn = get_pg_connection()
    cursor = conn.cursor()
    limit = period_to_limit(period)
    cursor.execute("""
        SELECT open_time, open, high, low, close, volume
        FROM candles
        WHERE symbol=%s AND interval=%s
        ORDER BY open_time DESC
        LIMIT %s
    """, (symbol, interval, limit))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Candles non trouvées")
    df = pd.DataFrame(rows, columns=["open_time","open","high","low","close","volume"])
    df = df.sort_values("open_time")
    df["date"] = pd.to_datetime(df["open_time"])
    return df

@app.get("/")
def home():
    return {
        "message": "CryptoBot API PG running",
        "cryptos": AVAILABLE_CRYPTOS,
        "intervals": AVAILABLE_INTERVALS,
        "periods": AVAILABLE_PERIODS
    }

@app.get("/stats")
def stats(symbol: str = Query("BTCUSDT"), interval: str = Query("1h")):
    """Pour l’onglet Dashboard"""
    dashboard = fetch_dashboard(symbol, interval)
    dashboard["symbol"] = symbol
    dashboard["interval"] = interval
    return dashboard

@app.get("/charts")
def charts(symbol: str = Query("BTCUSDT"), interval: str = Query("1h"), period: str = Query("1D")):
    """Pour les graphes et le ML (historique complet + indicateurs)"""
    df_candles = fetch_candles(symbol, interval, period)
    df_ml = fetch_ml_features(symbol, interval, period)

    # Merge ML features sur candles pour le Streamlit ML tab
    df = pd.merge(df_candles,df_ml[["date", "return_1h", "ma_24", "volatility_24", "ema_20", "rsi"]],on="date",how="left")

    df = df.fillna(0)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")

@app.get("/signals")
def signals(symbol: str = Query("BTCUSDT"), interval: str = Query("1h")):
    """Signal basé sur EMA/RSI pour le dashboard"""
    dashboard = fetch_dashboard(symbol, interval)
    last_close = dashboard["last_price"]
    last_ema = dashboard["ema_20"]
    last_rsi = dashboard["rsi"]

    if last_close > last_ema and 50 <= last_rsi < 70:
        signal = "BUY"
        reason = "Prix au-dessus de l’EMA et RSI haussier"
    elif last_close < last_ema and 30 < last_rsi < 50:
        signal = "SELL"
        reason = "Prix en-dessous de l’EMA et RSI baissier"
    else:
        signal = "HOLD"
        reason = "Conditions intermédiaires ou marché incertain"

    return {
        "signal": signal,
        "close": round(last_close,2),
        "ema_20": round(last_ema,2),
        "rsi": round(last_rsi,2),
        "reason": reason
    }