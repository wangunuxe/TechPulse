import yfinance as yf
import pandas as pd

# TOP 50 GLOBAL TECH COMPANIES TICKER SYMBOLS
TOP_50_TECH_TICKERS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "NVDA",  # NVIDIA
    "GOOGL", # Alphabet (Google)
    "AMZN",  # Amazon
    "META",  # Meta (Facebook)
    "TSLA",  # Tesla
    "AVGO",  # Broadcom
    "ORCL",  # Oracle
    "ASML",  # ASML Holding
    "AMD",   # AMD
    "QCOM",  # Qualcomm
    "TXN",   # Texas Instruments
    "AMAT",  # Applied Materials
    "INTC",  # Intel
    "ADI",   # Analog Devices
    "LRCX",  # Lam Research
    "KLAC",  # KLA Corporation
    "SNPS",  # Synopsys
    "CDNS",  # Cadence Design
    "NXPI",  # NXP Semiconductors
    "MRVL",  # Marvell Technology
    "MPWR",  # Monolithic Power
    "FTNT",  # Fortinet
    "PANW",  # Palo Alto Networks
    "CRM",   # Salesforce
    "NOW",   # ServiceNow
    "WDAY",  # Workday
    "SNOW",  # Snowflake
    "DDOG",  # Datadog
    "NET",   # Cloudflare
    "MDB",   # MongoDB
    "TEAM",  # Atlassian
    "ZM",    # Zoom
    "SHOP",  # Shopify
    "SE",    # Sea Limited
    "BIDU",  # Baidu
    "TCEHY", # Tencent
    "BABA",  # Alibaba
    "9988.HK", # Alibaba HK
    "035420.KS", # NAVER (Korea)
    "005930.KS", # Samsung (Korea)
    "SAP",   # SAP (Germany)
    "NOKIA", # Nokia
    "ERIC",  # Ericsson
    "STM",   # STMicroelectronics
    "INFY",  # Infosys (India)
    "WIT",   # Wipro (India)
    "UBER",  # Uber
    "LYFT",  # Lyft
]

# DOWNLOAD STOCK PRICE

def download_price(ticker: str) ->pd.DataFrame:
    """
    Download today's stock price for a given ticker.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d") # Only fetch today's data
    hist["ticker"] = ticker # Add ticker column
    return hist

# FETCH ALL 50 STOCKS
def fetch_all_stock():
    """
    Fetch stock prices for all top 50 tech companies.
    """
    all_data = []

    for ticker in TOP_50_TECH_TICKERS:
        try:
            df = download_price(ticker)
            if not df.empty:
                all_data.append(df)
                print(f"✅ {ticker} fetched successfully")
            else:
                print(f"⚠️ {ticker} returned empty data")
        except Exception as e:
            print(f"❌ {ticker} failed: {e}")
    # Combine all data into one DataFrame
    if all_data:
        combined = pd.concat(all_data) # Merge all 50 DataFrames into one big DataFrame
        print(f"\n📊 Total records fetched: {len(combined)}")  # Print total number of rows
        print(combined[["ticker", "Open", "High", "Low", "Close", "Volume"]]) # Only display these 6 columns (ignore the rest)
    else:
        print("No data fetched.")


if __name__ == "__main__":
    # data = download_price("LYFT")
    # print(data.columns.tolist())
    # print(data)
    # print(data.T) # Transpose — easier to read all fields
    fetch_all_stock()