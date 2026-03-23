import pandas as pd
from src.storage.pg import get_pg_connection


INSERT_SQL = """
INSERT INTO dashboard_metrics (
    symbol, interval,
    last_price, max_price, min_price, avg_volume, ema_20, rsi
)
VALUES (%s,%s,%s,%s,%s,%s)
ON CONFLICT (symbol, interval) DO UPDATE SET
    last_price = EXCLUDED.last_price,
    max_price = EXCLUDED.max_price,
    min_price = EXCLUDED.min_price,
    avg_volume = EXCLUDED.avg_volume,
    ema_20 = EXCLUDED.ema_20,
    rsi = EXCLUDED.rsi;
"""


def run_dashboard_transform(symbol: str, interval: str):
    conn = get_pg_connection()
    cursor = conn.cursor()

    # récupérer les données depuis candles
    cursor.execute("""
        SELECT open_time, open, high, low, close, volume
        FROM candles
        WHERE symbol = %s AND interval = %s
        ORDER BY open_time
    """, (symbol, interval))

    rows = cursor.fetchall()

    if not rows:
        print("Pas de données")
        return

    df = pd.DataFrame(rows, columns=[
        "open_time", "open", "high", "low", "close", "volume"
    ])

    df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df["rsi"] = 100 - (100 / (1 + rs))
    df["rsi"] = df["rsi"].fillna(50)

    metrics = (
        symbol,
        interval,
        float(df["close"].iloc[-1]),
        float(df["high"].max()),
        float(df["low"].min()),
        float(df["volume"].mean())
    )

    cursor.execute(INSERT_SQL, metrics)
    conn.commit()

    cursor.close()
    conn.close()

    print("Dashboard metrics updated")