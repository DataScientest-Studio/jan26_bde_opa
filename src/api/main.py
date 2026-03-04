from pydantic import BaseModel
from src.models.predict_model import load_model, predict_one
from fastapi import FastAPI
from src.storage.pg import get_pg_connection

app = FastAPI()
model = load_model()

class PredictionRequest(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/symbols")
def list_symbols():

    conn = get_pg_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT symbol, interval, COUNT(*) as n
        FROM candles
        GROUP BY symbol, interval
        ORDER BY n DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "symbol": r[0],
            "interval": r[1],
            "count": r[2]
        })

    return {"data": data}


@app.get("/candles")
def get_candles(symbol: str, interval: str, limit: int = 100):

    conn = get_pg_connection()
    cursor = conn.cursor()

    query = """
        SELECT symbol, interval, open_time, open, high, low, close, volume
        FROM candles
        WHERE symbol = %s AND interval = %s
        ORDER BY open_time DESC
        LIMIT %s
    """

    cursor.execute(query, (symbol, interval, limit))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    data = []
    for r in rows:
        data.append({
            "symbol": r[0],
            "interval": r[1],
            "open_time": r[2],
            "open": r[3],
            "high": r[4],
            "low": r[5],
            "close": r[6],
            "volume": r[7],
        })

    return {"data": data}


@app.get("/stats")
def get_stats(symbol: str, interval: str):

    conn = get_pg_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as n,
            MIN(open_time),
            MAX(open_time),
            MIN(low),
            MAX(high)
        FROM candles
        WHERE symbol = %s AND interval = %s
    """, (symbol, interval))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "symbol": symbol,
        "interval": interval,
        "count": row[0],
        "min_open_time": row[1],
        "max_open_time": row[2],
        "min_low": row[3],
        "max_high": row[4]
    }

@app.post("/predict")
def predict(data: PredictionRequest):

    result = predict_one(model, data.model_dump())

    return result