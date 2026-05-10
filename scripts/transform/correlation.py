import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from scripts.load import read_raw

def transform_correlation():
    df = read_raw()
    #Reshape the data so that each column represents one company (pivot)
    result = df.pivot_table(
        index="date",
        columns="ticker",
        values="close"
    ).copy()
    result["date"] = df.index
    # print(f"pivot shape: {result.shape}")
    # print(f"thresh: {len(result)//2}")
    # print(f"valid values per column:\n{result.count()}")

    # 用实际有效值的最大数量作为基准
    # max_valid = result.count().max()  # = 251
    # # 保留有效值超过80%的列 = 251 * 0.8 = 200
    # # calculate the correlation between these ticker :Pearson Correlation Coefficient
    # # drop columns which have LESS THAN len(result)//2 valid values
    # Correlation = result.dropna(axis=1, thresh=int(max_valid * 0.8)).corr()

    #删除非美股（时区不同的股票）
    EXCLUDE = ["005930.KS", "035420.KS", "9988.HK"]
    pivot_us = result.drop(columns=EXCLUDE, errors="ignore")

    #删除有NaN的行
    pivot_clean = pivot_us.dropna()

    #计算相关性
    correlation_matrix = pivot_clean.corr()
    return correlation_matrix

def get_top_correlation(top_n=3):
    result = []
    corr_matrix=transform_correlation()
    for ticker in corr_matrix.columns:
        # 排除自己（相关性=1）
        top = corr_matrix[ticker].drop(ticker).nlargest(top_n)
        for related_ticker, value in top.items():
            result.append({
                "ticker": ticker,
                "related_ticker": related_ticker,
                "correlation": round(value, 3)
            })
    return pd.DataFrame(result)

if __name__ == "__main__":
    clean_data = transform_correlation()
    print(clean_data)
    top_corr=get_top_correlation()
    print(top_corr)

