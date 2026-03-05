# src/processors/preprocess.py
from typing import Dict, Any

def preprocess_raw_kline(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "symbol": str(doc["symbol"]),
        "interval": str(doc["interval"]),
        "open_time": int(doc["open_time"]),
        "open": float(doc["open"]),
        "high": float(doc["high"]),
        "low": float(doc["low"]),
        "close": float(doc["close"]),
        "volume": float(doc["volume"]),
        "close_time": int(doc["close_time"]),
        "number_of_trades": int(doc.get("number_of_trades", 0) or 0),
        "ingested_at": int(doc.get("ingested_at", 0) or 0),
    }