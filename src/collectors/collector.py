from binance_collector import get_klines
from mongo_connexion import get_mongo_client, get_database, insert_data

def run_collection(symbol: str, interval: str, limit: int = 500):

    # 1. Get data
    df = get_klines(symbol=symbol, interval=interval, limit=limit)

    # 2. Convert to dict
    records = df.to_dict(orient="records")

    # 3. Connect Mongo
    client = get_mongo_client()
    db = get_database(client)

    # Collection dynamique
    collection_name = f"raw_{symbol}_{interval}"
    collection = db[collection_name]

    # 4. Insert
    insert_data(collection, records)

    print(f"Data inserted for {symbol} - {interval}")

if __name__ == "__main__":
    run_collection("BTCUSDT", "1h")