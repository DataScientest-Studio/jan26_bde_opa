from ingest_historical import ingest_history
from datetime import datetime, timedelta

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"]
INTERVALS = ["1m", "5m", "15m", "1h", "4h", "1d"]

def now_minus(minutes):
    dt = datetime.utcnow() - timedelta(minutes=minutes)
    return int(dt.timestamp() * 1000)

def update():
    for symbol in SYMBOLS:
        for interval in INTERVALS:
            try:
                ingest_history(symbol, interval, now_minus(120))
            except Exception as e:
                print("Erreur:", e)

if __name__ == "__main__":
    update()