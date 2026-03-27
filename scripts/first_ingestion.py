from ingest_historical import ingest_history

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"]
INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]


START_DATES = {
    "1m": 7,    # 7 jours
    "5m": 30,
    "15m": 60,
    "1h": 180,
    "4h": 365,
    "1d": 1000
}

import time
from datetime import datetime, timedelta


def days_to_ms(days):
    dt = datetime.utcnow() - timedelta(days=days)
    return int(dt.timestamp() * 1000)


def run_full_ingestion():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            print(f"\n--- Ingestion {symbol} {interval} ---")

            start_time = days_to_ms(START_DATES[interval])

            try:
                ingest_history(symbol, interval, start_time)
            except Exception as e:
                print(f"Erreur {symbol} {interval}:", e)

            time.sleep(1)  # éviter rate limit


if __name__ == "__main__":
    run_full_ingestion()