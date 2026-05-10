import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.extract import fetch_all_stock

# ============================================
# GET ENGINE
# ============================================
load_dotenv(".env.local", override=True) #读取 .env 文件，把里面的变量加载到环境变量中

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
# ============================================
# LOAD RAW DATA
# ============================================
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
# ============================================
# READ RAW DATA
# ============================================

def read_raw() ->pd.DataFrame:
    """Read raw stock data from PostgreSQL."""
    engine = get_engine()
    # PostgreSQL → DataFrame
    df = pd.read_sql('SELECT * FROM raw_stock_prices ORDER BY ticker, "Date"', engine)

    # Rename all columns to lowercase
    df.columns = df.columns.str.lower()

    # Set date as index
    df = df.set_index("date")
    #print(df.columns.tolist())
    print(f"📊 {len(df)} records read from raw_stock_prices")
    return df

# ============================================
# LOAD TRANSFORMED DATA
# ============================================

def load_transformed(df: pd.DataFrame, table_name: str) -> None:
    """
    Generic function to load any transformed DataFrame into PostgreSQL.
    
    Args:
        df: transformed DataFrame to load
        table_name: target table name in PostgreSQL
    """
    engine = get_engine()
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",  # Replace table on each run
        index=False,
    )
    print(f"✅ {len(df)} records loaded into {table_name}")

def load_daily_return():
    from scripts.transform.daily_return import transform_intraday_return
    load_transformed(transform_intraday_return(), "transformed_daily_return")

def load_moving_average():
    from scripts.transform.moving_average import transform_moving_average
    load_transformed(transform_moving_average(),      "transformed_moving_average")

def load_volatility():
    from scripts.transform.volatility import transform_volatility
    load_transformed(transform_volatility(),          "transformed_volatility")

def load_volume_anomaly():
    from scripts.transform.volume_anomaly import transform_volume_anomaly
    load_transformed(transform_volume_anomaly(),      "transformed_volume_anomaly")

def load_sector_performance():
    from scripts.transform.sector_performance import transform_sector_performance
    load_transformed(transform_sector_performance(),  "transformed_sector_performance")

def load_correlation():
    from scripts.transform.correlation import transform_correlation
    load_transformed(transform_correlation(),         "transformed_correlation")

# ============================================
# READ TRANSFORMED DATA
# ============================================

def read_transformed(table_name: str) -> pd.DataFrame:
    """
    Generic function to read any transformed table from PostgreSQL.
    
    Args:
        table_name: source table name in PostgreSQL
    """
    engine = get_engine()
    df = pd.read_sql(
        f"SELECT * FROM {table_name}",
        engine,
    )
    print(f"📊 {len(df)} records read from {table_name}")
    return df

if __name__ == "__main__":
    # load_daily_return()
    # daily_return = read_transformed("transformed_daily_return")
    # print(daily_return.columns.tolist())
    # print(daily_return)

    load_moving_average()
    moving_average = read_transformed("transformed_moving_average")
    print(moving_average.columns.tolist())
    print(moving_average)

   
    # load_volatility()
    # volatility = read_transformed("transformed_volatility")
    # print(volatility.columns.tolist())
    # print(volatility)


    # load_volume_anomaly()
    # volume_anomaly  = read_transformed("transformed_volume_anomaly")
    # print(volume_anomaly.columns.tolist())
    # print(volume_anomaly)


    # load_sector_performance()
    # sector = read_transformed("transformed_sector_performance")
    # print(sector.columns.tolist())
    # print(sector)

    # load_correlation()
    # correlation = read_transformed("transformed_correlation")
    # print(correlation.columns.tolist())
    # print(correlation)


