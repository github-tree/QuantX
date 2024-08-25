import os


def generate_directory_structure(root_dir, directories, files):
    # 创建根目录
    os.makedirs(root_dir, exist_ok=True)

    # 创建子目录
    for directory in directories:
        dir_path = os.path.join(root_dir, directory)
        os.makedirs(dir_path, exist_ok=True)

    # 创建文件
    for file_name, content in files.items():
        file_path = os.path.join(root_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(content)


if __name__ == "__main__":
    root_dir = "quantitative_trading"
    directories = ["data", "strategy"]
    files = {
        "data/stock_data.csv": "Date,Open,High,Low,Close,Volume\n2021-01-01,100,105,95,102,100000\n2021-01-02,102,110,100,108,120000\n",
        "strategy/__init__.py": "",
        "strategy/moving_average_strategy.py": "import pandas as pd\nimport numpy as np\n\ndef moving_average_strategy(stock_data, short_window=20, long_window=50):\n    signals = pd.DataFrame(index=stock_data.index)\n    signals['signal'] = 0.0\n    \n    # 计算短期和长期移动平均线\n    signals['short_mavg'] = stock_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()\n    signals['long_mavg'] = stock_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()\n    \n    # 生成买入和卖出信号\n    signals['signal'][short_window:] = \\\n        np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)   \n    \n    signals['positions'] = signals['signal'].diff()\n    return signals\n",
        "main.py": "import pandas as pd\nimport matplotlib.pyplot as plt\nfrom strategy.moving_average_strategy import moving_average_strategy\n\n# 读取历史股票价格数据\nstock_data = pd.read_csv('data/stock_data.csv', index_col='Date', parse_dates=True)\n\n# 计算交易信号\nsignals = moving_average_strategy(stock_data)\n\n# 绘制交易信号图表\nfig, ax = plt.subplots(figsize=(10, 6))\nstock_data['Close'].plot(ax=ax, label='Close Price')\nsignals[['short_mavg', 'long_mavg']].plot(ax=ax, label='Moving Averages')\nax.plot(signals.loc[signals.positions == 1.0].index, \n        signals.short_mavg[signals.positions == 1.0],\n        '^', markersize=10, color='g', lw=0, label='Buy Signal')\nax.plot(signals.loc[signals.positions == -1.0].index, \n        signals.short_mavg[signals.positions == -1.0],\n        'v', markersize=10, color='r', lw=0, label='Sell Signal')\nplt.title('Moving Average Trading Strategy')\nplt.legend()\nplt.show()"
    }

    generate_directory_structure(root_dir, directories, files)
    print("目录及文件结构已成功生成！")
