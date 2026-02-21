import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg

# Trouve automatiquement la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

# Charge le .env en forçant l'override
load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_pg_connection():
    host = (os.getenv("PG_HOST", "127.0.0.1") or "").strip()
    port = (os.getenv("PG_PORT", "5432") or "").strip()
    dbname = (os.getenv("PG_DB", "trading") or "").strip()
    user = (os.getenv("PG_USER", "admin") or "").strip()
    password = (os.getenv("PG_PASSWORD", "admin") or "").strip()

    # Debug
    print("ENV_PATH =", ENV_PATH)
    print("PG_HOST  =", repr(host))
    print("PG_DB    =", repr(dbname))
    print("PG_USER  =", repr(user))
    print("PG_PASS length =", len(password))

    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )


def test_connection():
    conn = get_pg_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print("PostgreSQL connecté ✅", cur.fetchone())
    finally:
        conn.close()


if __name__ == "__main__":
    test_connection()




