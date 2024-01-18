import datetime
import pandas as pd
import talib
from db_select import *
import numpy as np

# 目前日期
current_date = datetime.date.today()  # 這裡改成今天的日期
# 策略設計
# 步驟1: 獲取股價數據
def get_stock_data(symbol):
    stock_data = select_data(symbol)
    return stock_data

# 步驟2: 計算技術指標
def calculate_technical_indicators(data):
    # RSI (相對強弱指標)
    data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

    # MA20 (移動平均線)
    data['MA20'] = talib.SMA(data['Adj Close'], timeperiod=20)

    # MA50 (移動平均線)
    data['MA50'] = talib.SMA(data['Adj Close'], timeperiod=50)

    # MACD (移動平均收斂與分歧)
    data['MACD'], data['Signal_Line'], _ = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # KD (隨機指標)
    data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Adj Close'], fastk_period=9, slowk_period=3, slowd_period=3)

    return data

# 步驟3: 制定交易策略
def generate_signals(data):
    # 這裡你可以根據你的策略定義買入和賣出的條件
    # 這只是一個簡單的例子，實際的策略可能會更複雜
    signals = pd.DataFrame(index=data.index)
   
    # 買入條件1：RSI小於30
    buy_condition1 = (data['RSI'] < 30)

    # 買入條件2：價格在今天的MA20金叉MA50
    buy_condition2 = (data['MA20'] > data['MA50']) & (data['MA20'].shift(1) < data['MA50'].shift(1))

    # 買入條件3：MACD金叉, MACD第二個條件是用來確保前一天跟今天發生金叉
    buy_condition3 = (data['MACD'] > data['Signal_Line']) & (data['MACD'].shift(1) < data['Signal_Line'].shift(1))

    # 買入條件4：隨機指標K穿越D
    buy_condition4 = (data['K'] > data['D']) & (data['K'].shift(1) < data['D'].shift(1)) & (data['K'] < 20)

    # 買入條件達成的數量
    signals['Buy_Conditions_Met'] = buy_condition1.astype(int) + buy_condition2.astype(int) + buy_condition3.astype(int) + buy_condition4.astype(int)

    signals['Buy_Signal'] = signals['Buy_Conditions_Met'] >= 2

    # 賣出條件1：RSI大於70
    sell_condition1 = (data['RSI'] > 70)

    # 賣出條件2：價格在今天的MA20死叉MA50
    sell_condition2 = (data['MA20'] < data['MA50']) & (data['MA20'].shift(1) > data['MA50'].shift(1))

    # 賣出條件3：MACD死叉, MACD第二個條件是用來確保前一天跟今天發生死叉
    sell_condition3 = (data['MACD'] < data['Signal_Line']) & (data['MACD'].shift(1) > data['Signal_Line'].shift(1))

    # 賣出條件4：隨機指標K穿越D，且目前處於超買區域
    sell_condition4 = (data['K'] < data['D']) & (data['K'].shift(1) > data['D'].shift(1)) & (data['K'] > 80)

    # 賣出條件達成的數量
    signals['Sell_Conditions_Met'] = sell_condition1.astype(int) + sell_condition2.astype(int) + sell_condition3.astype(int) + sell_condition4.astype(int)

    signals['Sell_Signal'] = signals['Sell_Conditions_Met'] >= 2

    return signals

# 步驟4: 主程式
def main():
    total_signal = pd.DataFrame()
    total_stock_data = []
    all_data = select_data()
    for symbol in select_stock_n():
        # 設定參數
        # 股票代號
        try:
            # 獲取股價數據
            stock_data = all_data.loc[all_data['stock_n'] == symbol]

            # 計算技術指標
            stock_data = calculate_technical_indicators(stock_data)
            # 生成交易信號
            signals = generate_signals(stock_data)
            signals.reset_index(inplace=True)
            signals['symbol_with_date'] = signals['Date']
            signals['SYMBOL'] = symbol  # 寫入股票代號
            total_signal = pd.concat([total_signal, signals])
            total_stock_data.append(stock_data)

        except Exception as e :
            continue
    # 合併列表中的 DataFrame
    combined_signal = pd.DataFrame(total_signal)
    combined_signal.to_csv('origin_combine.csv')
    combined_signal = combined_signal[combined_signal['Buy_Signal'] | combined_signal['Sell_Signal']]

    combined_signal = combined_signal.reindex(["SYMBOL","Date","Buy_Conditions_Met","Buy_Signal","Sell_Conditions_Met","Sell_Signal"], axis="columns")
    combined_signal = combined_signal.loc[combined_signal['Date'] == '2024-01-15']

    combined_signal['Action'] = np.where(combined_signal['Buy_Signal'] == True, '買入時機', np.where(combined_signal['Sell_Signal'] == True, '賣出時機', '繼續持有'))
    for index, row in combined_signal.iterrows():
        print(f"股票代號: {row['SYMBOL']}")
        print(f"Date: {row['Date']}")
        print(f"關注: {row['Action']}")
        print("-------------------")
    return ""
# if __name__ == "__main__":
#     main()