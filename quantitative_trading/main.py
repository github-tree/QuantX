import matplotlib.pyplot as plt
from data.data_handler import fetch_stock_data
from strategy.strategy_handler import moving_average_strategy

if __name__ == "__main__":
    ticker = "AAPL"  # 苹果公司的股票代码
    start_date = "2021-01-01"
    end_date = "2022-01-01"
    file_path = "data/stock_data.csv"

    stock_data = fetch_stock_data(ticker, start_date, end_date, file_path)

    signals = moving_average_strategy(stock_data)

    fig, ax = plt.subplots(figsize=(10, 6))
    stock_data['Close'].plot(ax=ax, label='Close Price')    #收盘价
    signals[['short_mavg', 'long_mavg']].plot(ax=ax, label='Moving Averages')   #短、长期移动平均
    ax.plot(signals.loc[signals.positions == 1.0].index,
            signals.short_mavg[signals.positions == 1.0],
            '^', markersize=10, color='g', lw=0, label='Buy Signal')    #买入信号
    ax.plot(signals.loc[signals.positions == -1.0].index,
            signals.short_mavg[signals.positions == -1.0],
            'v', markersize=10, color='r', lw=0, label='Sell Signal')   #卖出信号
    plt.title('Moving Average Trading Strategy')    #移动平均线交易策略
    plt.legend()
    plt.show()