# src/collectors/binance_collector.py
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
        params["startTime"] = start_time_ms
    if end_time_ms is not None:
        params["endTime"] = end_time_ms

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
