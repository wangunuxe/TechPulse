import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from scripts.load import read_raw

def transform_moving_average() -> pd.DataFrame:
    """
    Calculate 7-day and 30-day Simple moving average for each stock.

    Input columns required: ticker, Close, Date(index)
    Output columns added: MA7, MA30, trend
    """
    df = read_raw()
    result = df.copy()
    result["MA7"] = df.groupby("ticker")["close"].transform(lambda x: x.rolling(window=7).mean())

    result["MA30"] = df.groupby("ticker")["close"].transform(lambda x: x.rolling(window=30).mean())

    # Determine trend: MA7 > MA30 = Uptrend, MA7 < MA30 = Downtrend
    result["trend"] = result.apply(lambda row : "Uptrend" if row["MA7"] > row["MA30"] else ("Downtrend" if row["MA7"] < row["MA30"] else "Neutral"), axis = 1)

    return result

if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))

    from scripts.extract import fetch_all_stock
    raw_data = fetch_all_stock()
    if raw_data is not None:
        clean_data = transform_moving_average()
        print(clean_data)
        print(clean_data.columns.tolist())
    else:
        print(f"raw_data failed to fetch")

