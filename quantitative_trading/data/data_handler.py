import os
import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker, start_date, end_date, file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print("从文件中加载历史股票数据...")
        stock_data = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    else:
        print("通过接口获取历史股票数据...")
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data.to_csv(file_path)
    return stock_data
