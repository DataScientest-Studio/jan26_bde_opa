from dotenv import load_dotenv
load_dotenv()

import os
import psycopg2
from src.storage.mongo import get_database

INSERT_SQL = """
INSERT INTO candles
(symbol, interval, open_time, open, high, low, close, volume, close_time, number_of_trades, ingested_at)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (symbol, interval, open_time) DO NOTHING;
"""

def get_pg_connection_direct():
    # On lit .env mais on garde des defaults sûrs (et ASCII)
    host = os.getenv("PG_HOST", "127.0.0.1").strip()
    port = int(os.getenv("PG_PORT", "5432").strip())
    dbname = os.getenv("PG_DB", "trading").strip()
    user = os.getenv("PG_USER", "admin").strip()
    password = os.getenv("PG_PASSWORD", "admin").strip()

    # Si jamais un caractère invisible se balade, on nettoie fort
    host = host.replace("\ufeff", "")
    dbname = dbname.replace("\ufeff", "")
    user = user.replace("\ufeff", "")
    password = password.replace("\ufeff", "")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )

def load(symbol="BTCUSDT", interval="1h"):
    # Mongo
    db = get_database()
    col = db["raw_binance_klines"]

    # Postgres (direct, sans pg.py)
    conn = get_pg_connection_direct()
    cur = conn.cursor()

    q = {"symbol": symbol, "interval": interval}
    cursor = col.find(q)

    seen = 0
    inserted = 0

    for doc in cursor:
        seen += 1
        row = (
            doc["symbol"],
            doc["interval"],
            int(doc["open_time"]),
            float(doc["open"]),
            float(doc["high"]),
            float(doc["low"]),
            float(doc["close"]),
            float(doc["volume"]),
            int(doc["close_time"]),
            int(doc.get("number_of_trades")) if doc.get("number_of_trades") is not None else None,
            int(doc.get("ingested_at")) if doc.get("ingested_at") is not None else None,
        )
        cur.execute(INSERT_SQL, row)
        inserted += cur.rowcount

        if seen % 500 == 0:
            conn.commit()

    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Mongo read: {seen} | Postgres inserted: {inserted}")

if __name__ == "__main__":
    load()
