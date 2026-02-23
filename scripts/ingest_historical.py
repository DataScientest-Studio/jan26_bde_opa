from dotenv import load_dotenv
load_dotenv()

import time
from datetime import datetime, timezone

from src.collectors.binance_collector import get_klines
from src.storage.mongo import get_database


def to_ms(dt: datetime) -> int:
    return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)


def ingest(symbol="BTCUSDT", interval="1h"):
    db = get_database()
    collection = db["raw_binance_klines"]

    start_dt = datetime(2024, 1, 1)
    end_dt = datetime(2024, 2, 1)

    start_ms = to_ms(start_dt)
    end_ms = to_ms(end_dt)

    cursor = start_ms
    total = 0

    print("📥 Début ingestion historique...")

    while cursor < end_ms:
        candles = get_klines(
            symbol=symbol,
            interval=interval,
            start_time_ms=cursor,
            end_time_ms=end_ms,
            limit=1000,
        )

        if not candles:
            break

        docs = []
        for c in candles:
            docs.append({
                "symbol": symbol,
                "interval": interval,
                "open_time": c[0],
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5]),
                "close_time": c[6],
                "number_of_trades": c[8],
                "ingested_at": int(time.time() * 1000),
            })

        collection.insert_many(docs, ordered=False)
        total += len(docs)

        cursor = candles[-1][6] + 1
        time.sleep(0.2)

    print(f"✅ Ingestion terminée : {total} documents insérés")


if __name__ == "__main__":
    ingest()
    