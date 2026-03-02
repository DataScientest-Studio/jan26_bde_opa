from datetime import datetime, timezone
from typing import List, Tuple

from pymongo import ReturnDocument

from src.storage.mongo import get_database
from src.storage.pg import get_pg_connection
from src.processors.preprocess import preprocess_raw_kline


INSERT_SQL = """
INSERT INTO candles (
    symbol, interval, open_time,
    open, high, low, close, volume,
    close_time, number_of_trades, ingested_at
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (symbol, interval, open_time) DO NOTHING;
"""


def claim_next_batch(db):
    """
    Récupère le prochain batch pending et le passe en processing (atomique).
    """
    return db.etl_batch_logs.find_one_and_update(
        {"status": "pending"},
        {"$set": {"status": "processing", "started_at": datetime.now(timezone.utc)}},
        sort=[("created_at", 1)],
        return_document=ReturnDocument.AFTER,
    )


def run_batch():
    db = get_database()
    pg_conn = get_pg_connection()
    cursor = pg_conn.cursor()

    batch = claim_next_batch(db)

    if not batch:
        print("No pending batch found.")
        cursor.close()
        pg_conn.close()
        return

    batch_id = batch["batch_id"]
    symbol = batch["symbol"]
    interval = batch["interval"]

    print(f"Processing batch: {batch_id} ({symbol} / {interval})")

    counts = {"read": 0, "attempted_insert": 0}

    try:
        raw_docs = db["raw_binance_klines"].find({"symbol": symbol, "interval": interval})

        rows: List[Tuple] = []

        for doc in raw_docs:
            counts["read"] += 1
            row = preprocess_raw_kline(doc)

            rows.append(
                (
                    row["symbol"],
                    row["interval"],
                    row["open_time"],
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row["volume"],
                    row["close_time"],
                    row.get("number_of_trades"),
                    row.get("ingested_at"),
                )
            )

        if rows:
            cursor.executemany(INSERT_SQL, rows)
            pg_conn.commit()
            counts["attempted_insert"] = len(rows)

        db.etl_batch_logs.update_one(
            {"batch_id": batch_id},
            {
                "$set": {
                    "status": "processed",
                    "finished_at": datetime.now(timezone.utc),
                    "counts": counts,
                }
            },
        )

        print("Batch processed successfully.")
        print("Counts:", counts)

    except Exception as e:
        pg_conn.rollback()

        db.etl_batch_logs.update_one(
            {"batch_id": batch_id},
            {
                "$set": {
                    "status": "error",
                    "finished_at": datetime.now(timezone.utc),
                    "error": str(e),
                    "counts": counts,
                }
            },
        )

        print(f"Batch failed: {e}")
        raise

    finally:
        cursor.close()
        pg_conn.close()