from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient

def export_sql(symbol="BTCUSDT", interval="1h", out_path="reports/load_candles.sql"):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    mongo_db = os.getenv("MONGO_DB", "cryptobot")

    client = MongoClient(mongo_uri)
    db = client[mongo_db]
    col = db["raw_binance_klines"]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    q = {"symbol": symbol, "interval": interval}
    cursor = col.find(q)

    n = 0
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("-- Auto-generated from Mongo raw_binance_klines\n")
        f.write("BEGIN;\n")

        for doc in cursor:
            n += 1
            open_time = int(doc["open_time"])
            open_ = float(doc["open"])
            high = float(doc["high"])
            low = float(doc["low"])
            close = float(doc["close"])
            volume = float(doc["volume"])
            close_time = int(doc["close_time"])
            number_of_trades = int(doc.get("number_of_trades")) if doc.get("number_of_trades") is not None else "NULL"
            ingested_at = int(doc.get("ingested_at")) if doc.get("ingested_at") is not None else "NULL"

            # SQL INSERT (safe enough here because symbol/interval are fixed strings)
            f.write(
                "INSERT INTO candles (symbol, interval, open_time, open, high, low, close, volume, close_time, number_of_trades, ingested_at) "
                f"VALUES ('{symbol}', '{interval}', {open_time}, {open_}, {high}, {low}, {close}, {volume}, {close_time}, {number_of_trades}, {ingested_at}) "
                "ON CONFLICT (symbol, interval, open_time) DO NOTHING;\n"
            )

        f.write("COMMIT;\n")

    client.close()
    print(f"✅ SQL file generated: {out_path} | rows: {n}")

if __name__ == "__main__":
    export_sql()
    