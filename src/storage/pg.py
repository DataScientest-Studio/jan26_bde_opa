import os
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

def _clean(v: str, default: str) -> str:
    if v is None:
        return default
    return str(v).strip().replace("\ufeff", "")  

def get_pg_connection():
    host = _clean(os.getenv("PG_HOST"), "127.0.0.1")
    port = int(_clean(os.getenv("PG_PORT"), "5432"))
    dbname = _clean(os.getenv("PG_DB"), "trading")
    user = _clean(os.getenv("PG_USER"), "admin")
    password = _clean(os.getenv("PG_PASSWORD"), "admin")

    print("PG_HOST repr:", repr(host))
    print("PG_PORT repr:", repr(str(port)))
    print("PG_DB   repr:", repr(dbname))
    print("PG_USER repr:", repr(user))
    print("PG_PASS repr:", repr(password))

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )



