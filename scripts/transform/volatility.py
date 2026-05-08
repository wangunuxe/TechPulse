import pandas as pd

def transform_volatility(df: pd.DataFrame):
    """
    
    """
    # overnight_return :(Close今 - Close昨) / Close昨
    result = df[["Close", "ticker"]].copy()
    #result["overnight_return"] = df.groupby("ticker")["Close"].transform(lambda x : x.diff()/x.shift(1))
    result["overnight_return"] = df.groupby("ticker")["Close"].transform(lambda x: x.pct_change())

    # volatility
    result["volatility"] = result.groupby("ticker")["overnight_return"].transform(lambda x : x.rolling(window=30).std())

    # risk_level
    result["risk_level"] = result["volatility"].apply(lambda x :"Unknown" if pd.isna(x) 
    else ( "Low Risk" if x < 0.01 
    else ("Medium Risk" if x < 0.03 else "High Risk")))

    return result

if __name__ == "__main__" :
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    from scripts.extract import fetch_all_stock
    raw_data = fetch_all_stock()
    if raw_data is not None:
        clean_data=transform_volatility(raw_data)
        print(clean_data)
    else:
        print("The raw_data failed to fetch")
    



