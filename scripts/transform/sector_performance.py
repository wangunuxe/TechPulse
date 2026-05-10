import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from scripts.load import read_raw
from scripts.transform.daily_return import transform_intraday_return

SECTOR_MAP = {
    # Semiconductor 半导体
    "NVDA":      "Semiconductor",  # NVIDIA
    "AMD":       "Semiconductor",  # AMD
    "INTC":      "Semiconductor",  # Intel
    "AVGO":      "Semiconductor",  # Broadcom
    "QCOM":      "Semiconductor",  # Qualcomm
    "TXN":       "Semiconductor",  # Texas Instruments
    "AMAT":      "Semiconductor",  # Applied Materials
    "LRCX":      "Semiconductor",  # Lam Research
    "KLAC":      "Semiconductor",  # KLA Corporation
    "ADI":       "Semiconductor",  # Analog Devices
    "NXPI":      "Semiconductor",  # NXP Semiconductors
    "MRVL":      "Semiconductor",  # Marvell Technology
    "MPWR":      "Semiconductor",  # Monolithic Power
    "ASML":      "Semiconductor",  # ASML Holding
    "STM":       "Semiconductor",  # STMicroelectronics
    "TSM":       "Semiconductor",  # Taiwan Semiconductor
    "005930.KS": "Semiconductor",  # Samsung

    # Software 软件
    "MSFT":      "Software",       # Microsoft
    "ORCL":      "Software",       # Oracle
    "CRM":       "Software",       # Salesforce
    "NOW":       "Software",       # ServiceNow
    "WDAY":      "Software",       # Workday
    "SNOW":      "Software",       # Snowflake
    "DDOG":      "Software",       # Datadog
    "MDB":       "Software",       # MongoDB
    "TEAM":      "Software",       # Atlassian
    "SNPS":      "Software",       # Synopsys
    "CDNS":      "Software",       # Cadence Design
    "FTNT":      "Software",       # Fortinet
    "PANW":      "Software",       # Palo Alto Networks
    "NET":       "Software",       # Cloudflare
    "SAP":       "Software",       # SAP

    # Consumer Tech 消费科技
    "AAPL":      "Consumer Tech",  # Apple
    "GOOGL":     "Consumer Tech",  # Alphabet
    "META":      "Consumer Tech",  # Meta
    "TSLA":      "Consumer Tech",  # Tesla
    "ZM":        "Consumer Tech",  # Zoom

    # E-Commerce 电商
    "AMZN":      "E-Commerce",     # Amazon
    "BABA":      "E-Commerce",     # Alibaba
    "9988.HK":   "E-Commerce",     # Alibaba HK
    "SHOP":      "E-Commerce",     # Shopify
    "SE":        "E-Commerce",     # Sea Limited
    "BIDU":      "E-Commerce",     # Baidu
    "TCEHY":     "E-Commerce",     # Tencent
    "035420.KS": "E-Commerce",     # NAVER

    # IT Services IT服务
    "INFY":      "IT Services",    # Infosys
    "WIT":       "IT Services",    # Wipro
    "ERIC":      "IT Services",    # Ericsson

    # Mobility 出行
    "UBER":      "Mobility",       # Uber
    "LYFT":      "Mobility",       # Lyft
}

def transform_sector_performance():
    """
    Calculate average intraday return per sector:
        get intraday_return_pct
        Map each ticker to its sector using SECTOR_MAP
        Group by sector and calculate average return
        Rank sectors from best to worst performance
    """
    df = transform_intraday_return()
    result = df[["intraday_return_pct", "ticker"]].copy()
    result["date"] = df.index
    #Map each ticker to its sector
    result["sector"] = result["ticker"].map(SECTOR_MAP)

    #Group by sector and calculate average return; return a series
    sector_performance = result.groupby("sector")["intraday_return_pct"].mean().round(2).reset_index()

    # rename column and rank sectors by perfomance
    sector_performance.columns = ["sector", "avg_intraday_return_pct"]
    sector_performance = sector_performance.sort_values("avg_intraday_return_pct", ascending=False).reset_index(drop=True)

    # Add rank columnnn
    sector_performance["rank"] = sector_performance.index + 1

    return sector_performance
    
if __name__ == "__main__":
    clean_data = transform_sector_performance()
    print(clean_data)