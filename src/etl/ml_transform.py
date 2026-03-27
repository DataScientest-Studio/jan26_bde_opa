import pandas as pd
from src.storage.pg import get_pg_connection


INSERT_SQL = """
INSERT INTO ml_features (
    symbol,
    interval,
    open_time,
    close,
    return_1h,
    ma_24,
    volatility_24,
    ema_20,
    rsi
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (symbol, interval, open_time) DO NOTHING;
"""


def run_ml_transform():
    conn = get_pg_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT symbol, interval
            FROM candles
            ORDER BY symbol, interval
        """)
        pairs = cursor.fetchall()

        if not pairs:
            print("Pas de données dans candles")
            return

        total_inserted = 0

        for symbol, interval in pairs:
            cursor.execute(
                """
                SELECT open_time, close
                FROM candles
                WHERE symbol = %s AND interval = %s
                ORDER BY open_time
                """,
                (symbol, interval),
            )

            rows = cursor.fetchall()

            if not rows:
                continue

            df = pd.DataFrame(rows, columns=["open_time", "close"])
            df["close"] = df["close"].astype(float)

            # Features ML
            df["return_1h"] = df["close"].pct_change().fillna(0)
            df["ma_24"] = df["close"].rolling(24, min_periods=1).mean()
            df["volatility_24"] = df["return_1h"].rolling(24, min_periods=1).std().fillna(0)

            # EMA 20
            df["ema_20"] = df["close"].ewm(span=20, adjust=False).mean()

            # RSI 14
            delta = df["close"].diff()
            gain = delta.clip(lower=0)
            loss = -delta.clip(upper=0)

            avg_gain = gain.rolling(window=14, min_periods=14).mean()
            avg_loss = loss.rolling(window=14, min_periods=14).mean()

            rs = avg_gain / avg_loss.replace(0, pd.NA)
            df["rsi"] = 100 - (100 / (1 + rs))
            df["rsi"] = pd.to_numeric(df["rsi"], errors="coerce").fillna(50.0)

            data = [
                (
                    symbol,
                    interval,
                    row.open_time,
                    float(row.close),
                    float(row.return_1h),
                    float(row.ma_24),
                    float(row.volatility_24),
                    float(row.ema_20),
                    float(row.rsi),
                )
                for row in df.itertuples()
            ]

            cursor.executemany(INSERT_SQL, data)
            total_inserted += len(data)

        conn.commit()
        print(f"ML features updated: {total_inserted} lignes traitées")

    except Exception as e:
        conn.rollback()
        print("Erreur ML transform :", e)
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_ml_transform()