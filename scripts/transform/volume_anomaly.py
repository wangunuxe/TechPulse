import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from scripts.load import read_raw

def transform_volume_anomaly():
    """
    """
    df = read_raw()
    #print(df.index)
    result = df[["volume", "ticker"]].copy()
    #Average volume over the past 30 days
    result["avg_volume"] = df.groupby("ticker")["volume"].transform(lambda x : x.rolling(window=30).mean())
    #How many times today's volume is compared to the average
    result["volume_ratio"] = result["volume"] / result["avg_volume"]

    result["is_anomaly"] = result["volume_ratio"].apply(lambda x : "Unknown" if pd.isna(x) else("anomaly" if x > 2 else "normally") )

    return result

if __name__ == "__main__":
    # import sys
    # import os

    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    clean_data = transform_volume_anomaly()
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(clean_data)
