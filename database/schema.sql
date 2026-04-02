DROP TABLE IF EXISTS dashboard_metrics;
DROP TABLE IF EXISTS ml_features;
DROP TABLE IF EXISTS candles;

CREATE TABLE candles (
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time BIGINT NOT NULL,
    open DOUBLE PRECISION NOT NULL,
    high DOUBLE PRECISION NOT NULL,
    low DOUBLE PRECISION NOT NULL,
    close DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    close_time BIGINT NOT NULL,
    number_of_trades INTEGER,
    ingested_at BIGINT,
    PRIMARY KEY (symbol, interval, open_time)
);

CREATE TABLE dashboard_metrics (
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    last_price DOUBLE PRECISION,
    max_price DOUBLE PRECISION,
    min_price DOUBLE PRECISION,
    avg_volume DOUBLE PRECISION,
    ema_20 DOUBLE PRECISION,
    rsi DOUBLE PRECISION,
    PRIMARY KEY (symbol, interval)
);

CREATE TABLE ml_features (
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time BIGINT NOT NULL,
    close DOUBLE PRECISION,
    return_1h DOUBLE PRECISION,
    ma_24 DOUBLE PRECISION,
    volatility_24 DOUBLE PRECISION,
    ema_20 DOUBLE PRECISION,
    rsi DOUBLE PRECISION,
    PRIMARY KEY (symbol, interval, open_time)
);
