import pandas as pd
from src.storage.pg import get_pg_connection


INSERT_SQL = """
INSERT INTO dashboard_metrics (
    symbol,
    interval,
    last_price,
    max_price,
    min_price,
    avg_volume,
    ema_20,
    rsi
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (symbol, interval) DO UPDATE SET
    last_price = EXCLUDED.last_price,
    max_price = EXCLUDED.max_price,
    min_price = EXCLUDED.min_price,
    avg_volume = EXCLUDED.avg_volume,
    ema_20 = EXCLUDED.ema_20,
    rsi = EXCLUDED.rsi;
"""


def run_dashboard_transform():
    conn = get_pg_connection()
    cursor = conn.cursor()

    try:
        # récupérer toutes les combinaisons existantes
        cursor.execute("""
            SELECT DISTINCT symbol, interval
            FROM candles
            ORDER BY symbol, interval
        """)
        pairs = cursor.fetchall()

        if not pairs:
            print("Pas de données dans candles")
            return

        total_updated = 0

        for symbol, interval in pairs:
            cursor.execute(
                """
                SELECT open_time, open, high, low, close, volume
                FROM candles
                WHERE symbol = %s AND interval = %s
                ORDER BY open_time
                """,
                (symbol, interval),
            )

            rows = cursor.fetchall()

            if not rows:
                continue

            df = pd.DataFrame(
                rows,
                columns=["open_time", "open", "high", "low", "close", "volume"]
            )

            df["open"] = df["open"].astype(float)
            df["high"] = df["high"].astype(float)
            df["low"] = df["low"].astype(float)
            df["close"] = df["close"].astype(float)
            df["volume"] = df["volume"].astype(float)

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
            df["rsi"] = df["rsi"].fillna(50)

            metrics = (
                symbol,
                interval,
                float(df["close"].iloc[-1]),
                float(df["high"].max()),
                float(df["low"].min()),
                float(df["volume"].mean()),
                float(df["ema_20"].iloc[-1]),
                float(df["rsi"].iloc[-1]),
            )

            cursor.execute(INSERT_SQL, metrics)
            total_updated += 1

        conn.commit()
        print(f"Dashboard metrics updated: {total_updated} lignes")

    except Exception as e:
        conn.rollback()
        print("Erreur dashboard transform :", e)
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_dashboard_transform()