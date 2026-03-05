# src/collectors/binance_collector.py
import time
import requests
from typing import Optional, List, Any, Dict

BASE_URL = "https://api.binance.com"

def get_klines(
    symbol: str,
    interval: str,
    start_time_ms: Optional[int] = None,
    end_time_ms: Optional[int] = None,
    limit: int = 1000,
) -> List[List[Any]]:
    url = f"{BASE_URL}/api/v3/klines"
    params: Dict[str, Any] = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
    }
    if start_time_ms is not None:
        params["startTime"] = int(start_time_ms)
    if end_time_ms is not None:
        params["endTime"] = int(end_time_ms)

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def klines_to_docs(symbol: str, interval: str, klines: List[List[Any]]) -> List[Dict[str, Any]]:
    now_ms = int(time.time() * 1000)
    docs: List[Dict[str, Any]] = []
    for k in klines:
        docs.append({
            "source": "binance",
            "symbol": symbol.upper(),
            "interval": interval,
            "open_time": int(k[0]),
            "open": k[1],
            "high": k[2],
            "low": k[3],
            "close": k[4],
            "volume": k[5],
            "close_time": int(k[6]),
            "quote_asset_volume": k[7],
            "number_of_trades": int(k[8]),
            "taker_buy_base_asset_volume": k[9],
            "taker_buy_quote_asset_volume": k[10],
            "ingested_at": now_ms,
        })
    return docs