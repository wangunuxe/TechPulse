import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv() #读取 .env 文件，把里面的变量加载到环境变量中

DB_CONFIG = {
    "host":     os.getenv("STOCK_DB_HOST", "localhost"),  # Docker: stock-db, Local: localhost
    "port":     int(os.getenv("STOCK_DB_PORT", 5433)),    # Docker: 5432,    Local: 5433
    "dbname":   os.getenv("STOCK_DB_NAME", "stock"),
    "user":     os.getenv("STOCK_DB_USER", "stock"),
    "password": os.getenv("STOCK_DB_PASSWORD", "stock"),
}

def get_engine():
    """
    Create PostgreSQL connection engine.
    - Local testing: STOCK_DB_HOST=localhost, STOCK_DB_PORT=5433
    - Docker:        STOCK_DB_HOST=stock-db,  STOCK_DB_PORT=5432
    """
    return create_engine(
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )

# def get_engine():
#     """Create PostgreSQL connection."""
#     return create_engine(
#         f"postgresql://{os.getenv('STOCK_DB_USER')}:{os.getenv('STOCK_DB_PASSWORD')}"
#         f"@{os.getenv('STOCK_DB_HOST')}:5432/{os.getenv('STOCK_DB_NAME')}"
#     )

def clean_columns(df:pd.DataFrame) ->pd.DataFrame:
    """Clean column names before loading to PostgreSQL."""
    # Drop unnecessary columns
    df = df.drop(columns=["Dividends", "Stock Splits"])

    # Rename columns to lowercase with underscore
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

def load_raw(df: pd.DataFrame) -> None:
    """Load raw stock data into PostgreSQL."""
    engine = get_engine()
    df = clean_columns(df)
    # DataFrame → PostgreSQL
    df.to_sql(
        name = "raw_stock_prices",
        con=engine,
        if_exists="append",# 追加数据
        index=True, # 保留Date索引
    )
    print(f"✅ {len(df)} records loaded into raw_stock_prices")

def read_raw() ->pd.DataFrame:
    """Read raw stock data from PostgreSQL."""
    engine = get_engine()
    # PostgreSQL → DataFrame
    df = pd.read_sql("SELECT * FROM raw_stock_prices", engine)
    print(f"📊 {len(df)} records read from raw_stock_prices")
    return df

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from scripts.extract import fetch_all_stock

    # Step 1: Extract
    raw_data = fetch_all_stock()

    # Step 2: Load
    if raw_data is not None:
        load_raw(raw_data)

        # Step 3: Verify
        result = read_raw()
        print(result.head())