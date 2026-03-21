from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient, ASCENDING
import os


def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/").strip()
    return MongoClient(mongo_uri)


def get_database(db_name=None):
    client = get_mongo_client()
    db_name = (db_name or os.getenv("MONGO_DB", "cryptobot")).strip()
    return client[db_name]


def ensure_raw_klines_indexes(db):
    """
    Index unique pour éviter les doublons (symbol, interval, open_time)
    """
    col = db["raw_binance_klines"]
    col.create_index(
        [("symbol", ASCENDING), ("interval", ASCENDING), ("open_time", ASCENDING)],
        unique=True,
        name="uniq_symbol_interval_open_time"
    )
    return col


def test_connection():
    try:
        db = get_database()
        print("MongoDB connecté ✅")
        print("DB :", db.name)

        col = ensure_raw_klines_indexes(db)
        print("Collections :", db.list_collection_names())
        print("Indexes raw_binance_klines :", list(col.index_information().keys()))

    except Exception as e:
        print("Erreur connexion MongoDB ❌", e)

def insert_data(collection, data):
    if isinstance(data, list):
        collection.insert_many(data, ordered=False)
    else:
        collection.insert_one(data)

if __name__ == "__main__":
    test_connection()
