from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
import os


def get_mongo_client():
    """
    Retourne un client MongoDB.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    return MongoClient(mongo_uri)


def get_database(db_name="cryptobot"):
    client = get_mongo_client()
    return client[db_name]


def test_connection():
    try:
        db = get_database()
        collections = db.list_collection_names()
        print("MongoDB connecté ✅")
        print("Collections existantes :", collections)
    except Exception as e:
        print("Erreur connexion MongoDB ❌", e)


if __name__ == "__main__":
    test_connection()
