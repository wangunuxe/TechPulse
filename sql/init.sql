CREATE TABLE raw_stock_prices (
    date        TIMESTAMP,
    ticker      VARCHAR(20),
    open        FLOAT,
    close       FLOAT,
    volume      BIGINT,
    PRIMARY KEY (date, ticker)   # ← 主键
);
