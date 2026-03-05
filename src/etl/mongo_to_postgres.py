from datetime import datetime, timezone
from typing import List, Tuple, Optional, Dict, Any

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


def get_now():
    return datetime.now(timezone.utc)


def run_batch(symbol: Optional[str] = None, interval: Optional[str] = None):

    # Connexions
    db = get_database()
    pg_conn = get_pg_connection()

    started_at = get_now()
    counts = {"read": 0, "attempted_insert": 0}

    # Filtre Mongo
    mongo_filter: Dict[str, Any] = {}

    if symbol is not None:
        mongo_filter["symbol"] = symbol

    if interval is not None:
        mongo_filter["interval"] = interval

    # Log debut
    log_document = {
        "symbol": symbol if symbol else "ALL",
        "interval": interval if interval else "ALL",
        "status": "processing",
        "started_at": started_at,
        "finished_at": None,
        "counts": counts,
        "error": None,
    }

    log_id = db["etl_batch_logs"].insert_one(log_document).inserted_id

    try:
        total = db["raw_binance_klines"].count_documents(mongo_filter)

        print("Filtre Mongo :", mongo_filter)
        print("Nombre de documents trouves :", total)

        if total == 0:
            db["etl_batch_logs"].update_one(
                {"_id": log_id},
                {"$set": {"status": "no_data", "finished_at": get_now()}}
            )

            print("Aucune donnee a traiter")
            return

        cursor = pg_conn.cursor()

        raw_docs = db["raw_binance_klines"].find(mongo_filter).sort("open_time", 1)

        rows: List[Tuple] = []

        for doc in raw_docs:
            counts["read"] += 1

            row = preprocess_raw_kline(doc)

            rows.append(
                (
                    row["symbol"],
                    row["interval"],
                    int(row["open_time"]),
                    float(row["open"]),
                    float(row["high"]),
                    float(row["low"]),
                    float(row["close"]),
                    float(row["volume"]),
                    int(row["close_time"]),
                    row.get("number_of_trades"),
                    row.get("ingested_at"),
                )
            )

            if len(rows) >= 1000:
                cursor.executemany(INSERT_SQL, rows)
                pg_conn.commit()
                counts["attempted_insert"] += len(rows)
                rows = []

        # Dernier envoi
        if len(rows) > 0:
            cursor.executemany(INSERT_SQL, rows)
            pg_conn.commit()
            counts["attempted_insert"] += len(rows)

        cursor.close()

        db["etl_batch_logs"].update_one(
            {"_id": log_id},
            {
                "$set": {
                    "status": "processed",
                    "finished_at": get_now(),
                    "counts": counts,
                }
            },
        )

        print("ETL termine")
        print("Documents lus :", counts["read"])
        print("Insertions tentees :", counts["attempted_insert"])

    except Exception as e:
        pg_conn.rollback()

        db["etl_batch_logs"].update_one(
            {"_id": log_id},
            {
                "$set": {
                    "status": "error",
                    "finished_at": get_now(),
                    "error": str(e),
                }
            },
        )

        print("Erreur ETL :", e)
        raise

    finally:
        pg_conn.close()