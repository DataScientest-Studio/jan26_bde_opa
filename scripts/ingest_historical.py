import time
from pymongo import UpdateOne
from src.storage.mongo import get_database, ensure_raw_klines_indexes
from src.collectors.binance_collector import get_klines, klines_to_docs

def ingest_history(symbol: str, interval: str, start_time_ms: int, end_time_ms: int | None = None):
    db = get_database()
    col = ensure_raw_klines_indexes(db)

    total_fetched = 0
    total_upserted = 0
    cursor_start = start_time_ms

    while True:
        raw = get_klines(
            symbol=symbol,
            interval=interval,
            start_time_ms=cursor_start,
            end_time_ms=end_time_ms,
            limit=1000
        )
        if not raw:
            print("No more data. Stop.")
            break

        docs = klines_to_docs(symbol, interval, raw)
        total_fetched += len(docs)

        ops = [
            UpdateOne(
                {"symbol": d["symbol"], "interval": d["interval"], "open_time": d["open_time"]},
                {"$setOnInsert": d},
                upsert=True
            )
            for d in docs
        ]
        res = col.bulk_write(ops, ordered=False)
        total_upserted += res.upserted_count

        last_open_time = docs[-1]["open_time"]
        next_start = last_open_time + 1

        print(f"batch fetched={len(docs)} upserted={res.upserted_count} next_start={next_start}")

        if len(raw) < 1000:
            break

        cursor_start = next_start
        time.sleep(0.25)

    print(f"✅ DONE symbol={symbol} interval={interval} fetched={total_fetched} upserted={total_upserted}")

if __name__ == "__main__":
    # 2025-01-01T00:00:00Z en ms
    ingest_history("BTCUSDT", "1h", start_time_ms=1735689600000)
