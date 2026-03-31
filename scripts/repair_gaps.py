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

REPAIR_LOOKBACK = {
    "1m": timedelta(hours=6),
    "5m": timedelta(days=1),
    "15m": timedelta(days=2),
    "1h": timedelta(days=7),
    "4h": timedelta(days=30),
    "1d": timedelta(days=180),
}


def to_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def normalize_dt(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)

    raise ValueError(f"Type non géré pour open_time: {type(value)}")


def floor_datetime(dt: datetime, interval: str) -> datetime:
    dt = dt.astimezone(timezone.utc).replace(second=0, microsecond=0)

    if interval == "1m":
        return dt
    if interval == "5m":
        minute = (dt.minute // 5) * 5
        return dt.replace(minute=minute)
    if interval == "15m":
        minute = (dt.minute // 15) * 15
        return dt.replace(minute=minute)
    if interval == "1h":
        return dt.replace(minute=0)
    if interval == "4h":
        hour = (dt.hour // 4) * 4
        return dt.replace(hour=hour, minute=0)
    if interval == "1d":
        return dt.replace(hour=0, minute=0)

    raise ValueError(f"Intervalle inconnu: {interval}")


def build_expected_range(start: datetime, end: datetime, step: timedelta):
    values = []
    current = start
    while current <= end:
        values.append(current)
        current += step
    return values


def find_missing_ranges(existing_times, interval: str):
    step = INTERVAL_TO_DELTA[interval]

    if not existing_times:
        return []

    existing_set = set(existing_times)
    expected = build_expected_range(existing_times[0], existing_times[-1], step)

    missing = [dt for dt in expected if dt not in existing_set]
    if not missing:
        return []

    ranges = []
    range_start = missing[0]
    previous = missing[0]

    for current in missing[1:]:
        if current - previous == step:
            previous = current
        else:
            ranges.append((range_start, previous))
            range_start = current
            previous = current

    ranges.append((range_start, previous))
    return ranges


def repair_symbol_interval(symbol: str, interval: str):
    db = get_database()
    col = db["raw_klines"]

    now = datetime.now(timezone.utc)
    lookback_start = floor_datetime(now - REPAIR_LOOKBACK[interval], interval)

    docs = list(
        col.find(
            {
                "symbol": symbol,
                "interval": interval,
                "open_time": {"$gte": lookback_start}
            },
            {"_id": 0, "open_time": 1}
        ).sort("open_time", 1)
    )

    if not docs:
        print(f"[{symbol} {interval}] aucune donnée récente, rien à réparer")
        return

    existing_times = sorted(normalize_dt(doc["open_time"]) for doc in docs)
    existing_times = sorted(set(existing_times))

    start = floor_datetime(existing_times[0], interval)
    end = floor_datetime(existing_times[-1], interval)

    expected = build_expected_range(start, end, INTERVAL_TO_DELTA[interval])

    print(
        f"[{symbol} {interval}] existants={len(existing_times)} "
        f"attendus={len(expected)} "
        f"fenêtre={start.isoformat()} -> {end.isoformat()}"
    )

    missing_ranges = find_missing_ranges(existing_times, interval)

    if not missing_ranges:
        print(f"[{symbol} {interval}] aucun trou détecté")
        return

    print(f"[{symbol} {interval}] {len(missing_ranges)} trou(s) détecté(s)")

    for missing_start, missing_end in missing_ranges:
        safe_start = missing_start - (INTERVAL_TO_DELTA[interval] * 2)

        print(
            f"[{symbol} {interval}] réparation du trou "
            f"{missing_start.isoformat()} -> {missing_end.isoformat()} "
            f"(reprise depuis {safe_start.isoformat()})"
        )

        try:
            ingest_history(symbol, interval, to_ms(safe_start))
        except Exception as e:
            print(f"[{symbol} {interval}] erreur réparation: {e}")


def repair_gaps():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                repair_symbol_interval(symbol, interval)
            except Exception as e:
                print(f"[{symbol} {interval}] erreur globale: {e}")


if __name__ == "__main__":
    repair_gaps()