import pandas as pd

def transform_intraday_return(df: pd.DataFrame)->pd.DataFrame:
    """
    Calculate daily price change and percentage for each stock.

    Input columns required: ticker, Open, Close
    Output columns added: intraday_price_change, intraday_return_pct, status

    (Close - Open) / Open
    """
    result = df[["ticker", "Open", "Close"]].copy()
    result["intraday_price_change"] = (result["Close"] - result["Open"]).round(2)
    # Daily return = daily price change percentage
    result["intraday_return_pct"] = ((result["Close"] - result["Open"]) / result["Open"] * 100).round(2)

    result["status"] = result["intraday_return_pct"].apply(
        lambda x: "Gain" if x > 0 else ("Loss" if x < 0 else "Flat")
    )
    # Sort by return percentage (highest first)
    result = result.sort_values("intraday_return_pct", ascending=False).reset_index(drop=True)

    return result

if __name__ == "__main__":
    import sys
    import os

    # Add project root to path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    from scripts.extract import fetch_all_stock

    # Step 1: Extract
    raw_data = fetch_all_stock()

    # Step 2: Transform
    if raw_data is not None:
        result = transform_intraday_return(raw_data)

        print("\n🏆 Top 5 Gainers:")
        print(result.head())

        print("\n💀 Top 5 Losers:")
        print(result.tail())

        print(f"\n📊 Total: {len(result)} stocks processed")
