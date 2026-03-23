import pandas as pd
from src.storage.pg import get_pg_connection


INSERT_SQL = """
INSERT INTO ml_features (
    symbol, interval, open_time,
    close, return_1h, ma_24, volatility_24
)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (symbol, interval, open_time) DO NOTHING;
"""


def run_ml_transform(symbol: str, interval: str):
    conn = get_pg_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT open_time, close
        FROM candles
        WHERE symbol = %s AND interval = %s
        ORDER BY open_time
    """, (symbol, interval))

    rows = cursor.fetchall()

    if not rows:
        print("Pas de données")
        return

    df = pd.DataFrame(rows, columns=["open_time", "close"])

    # FEATURES ML
    df["return_1h"] = df["close"].pct_change().fillna(0)
    df["ma_24"] = df["close"].rolling(24, min_periods=1).mean()
    df["volatility_24"] = (df["return_1h"].rolling(24, min_periods=1).std().fillna(0))

    data = [
        (
            symbol,
            interval,
            int(row.open_time),
            float(row.close),
            float(row.return_1h),
            float(row.ma_24),
            float(row.volatility_24),
        )
        for row in df.itertuples()
    ]

    cursor.executemany(INSERT_SQL, data)
    conn.commit()

    cursor.close()
    conn.close()

    print("ML features updated")