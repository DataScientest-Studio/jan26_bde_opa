from src.storage.pg import get_pg_connection


def create_tables():
    conn = get_pg_connection()
    cursor = conn.cursor()

    # Table dashboard
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dashboard_metrics (
        symbol TEXT,
        interval TEXT,
        last_price FLOAT,
        max_price FLOAT,
        min_price FLOAT,
        avg_volume FLOAT,
        PRIMARY KEY (symbol, interval)
    );
    """)

    # Table ML
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ml_features (
        symbol TEXT,
        interval TEXT,
        open_time BIGINT,
        close FLOAT,
        return_1h FLOAT,
        ma_24 FLOAT,
        volatility_24 FLOAT,
        PRIMARY KEY (symbol, interval, open_time)
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Tables créées avec succès")


if __name__ == "__main__":
    create_tables()