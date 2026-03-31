from datetime import datetime, timedelta, timezone
from ingest_historical import ingest_history
from src.storage.mongo import get_database

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"]
INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]

INTERVAL_TO_DELTA = {
    "1m": timedelta(minutes=1),
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "1d": timedelta(days=1),
}

DEFAULT_LOOKBACK = {
    "1m": timedelta(hours=2),
    "5m": timedelta(hours=6),
    "15m": timedelta(hours=12),
    "1h": timedelta(days=7),
    "4h": timedelta(days=30),
    "1d": timedelta(days=180),
}

def dt_to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)

def get_start_time_ms(symbol: str, interval: str) -> int:
    db = get_database()
    col = db["raw_klines"]

    last_doc = col.find_one(
        {"symbol": symbol, "interval": interval},
        sort=[("open_time", -1)]
    )

    now = datetime.now(timezone.utc)

    if not last_doc:
        return dt_to_ms(now - DEFAULT_LOOKBACK[interval])

    last_open_time = last_doc["open_time"]
    if isinstance(last_open_time, str):
        last_open_time = datetime.fromisoformat(last_open_time.replace("Z", "+00:00"))

    start_dt = last_open_time - (INTERVAL_TO_DELTA[interval] * 2)
    return dt_to_ms(start_dt)

def update():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                start_ms = get_start_time_ms(symbol, interval)
                ingest_history(symbol, interval, start_ms)
                print(f"OK {symbol} {interval} from {start_ms}")
            except Exception as e:
                print(f"Erreur {symbol} {interval}: {e}")

if __name__ == "__main__":
    update()