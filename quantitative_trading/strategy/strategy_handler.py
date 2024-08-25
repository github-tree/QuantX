import pandas as pd
import numpy as np


def moving_average_strategy(stock_data, short_window=20, long_window=50):
    signals = pd.DataFrame(index=stock_data.index)
    signals['signal'] = 0.0

    # 计算短期和长期移动平均线
    signals['short_mavg'] = stock_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = stock_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # 生成买入和卖出信号
    signals.iloc[short_window:, signals.columns.get_loc('signal')] = \
        np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    signals['positions'] = signals['signal'].diff()
    return signals
