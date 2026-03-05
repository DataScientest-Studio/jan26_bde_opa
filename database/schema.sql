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
