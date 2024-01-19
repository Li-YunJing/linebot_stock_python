import datetime
import yfinance as yf
import requests
import pandas as pd
import datetime


today_date = datetime.date.today()
previous_date = today_date - datetime.timedelta(days=1)
url = "https://api.finmindtrade.com/api/v4/data"
parameter = {
    "dataset": "TaiwanStockInfo",
    "start_date": previous_date,
}
r = requests.get(url, params=parameter)
data = r.json()
stock_deal_info = data["data"]
df = pd.DataFrame(stock_deal_info)[["stock_id"]]


# 使用正則表達式從 stock_id 中提取僅數字部分
df["numeric_stock_id"] = df["stock_id"].str.extract('(\\d+)')


# 選擇並保留唯一的數字 stock_id 值
unique_numeric_stock_ids = df["numeric_stock_id"].unique()


current_date = datetime.date.today() 
stock_tw = []
data_list = []
for i in unique_numeric_stock_ids:
    stock_tw.append(f"{i}.TW")
    
stock_tw_df = pd.DataFrame()
for symbol in stock_tw:
    start_date = current_date
    stock_data = yf.download(symbol, start=start_date)
    stock_data['stock_n'] = symbol
    data_list.append(stock_data)
    stock_tw_df = pd.concat(data_list)

# 將索引還原為普通的列
stock_tw_df.reset_index(inplace=True)

# 重新排列欄位順序
new_order = ['stock_n', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
stock_tw_df = stock_tw_df[new_order]

# 寫入 CSV 檔案，設定 index 參數為 False
stock_tw_df.to_csv('testdata.csv', index=False)

print(stock_tw_df)