import psycopg2
from psycopg2 import sql
import pandas as pd
# 建立資料庫連線
def select_data():
    conn = psycopg2.connect(
        host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
        user="stock_zs94_user",
        password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
        database="stock_zs94"   
    )

    # 建立一個 cursor 物件
    cursor = conn.cursor()

    # 動態組合 SQL 查詢，使用 TO_CHAR 函數將日期格式化
    table_name = "stockdb"
    date_format = "YYYY-MM-DD"  # 你想要的日期格式
    sql_query = f"SELECT stock_n, TO_CHAR(date, '{date_format}') AS formatted_date, open, high, low, close, \"Adj Close\", volume FROM {table_name}"
    cursor.execute(sql_query)
    # 獲取所有結果
    stock_data = cursor.fetchall()
    stock_data = pd.DataFrame(stock_data)
    stock_data.columns = ['stock_n', 'Date', 'Open', 'High', 'Low', 'Close','Adj Close', 'Volume']
    stock_data.reset_index(drop=True)
    stock_data.set_index('Date', inplace=True)
    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()

    return stock_data

def select_stock_n():
    conn = psycopg2.connect(
        host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
        user="stock_zs94_user",
        password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
        database="stock_zs94"   
    )

    # 建立一個 cursor 物件
    cursor = conn.cursor()

    # 動態組合 SQL 查詢唯一值
    table_name = "stockdb"
    sql_query = f"SELECT DISTINCT stock_n FROM {table_name}"
    cursor.execute(sql_query)
    # 獲取所有結果
    unique_stock_name = cursor.fetchall()

    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()
    unique_stock_name = [item[0] for item in unique_stock_name]
    return unique_stock_name


# import yfinance as yf
# result = select_data('2330.TW')
# print(result)

# stock_data = yf.download('2330.TW', start='2024-01-05')
# print(stock_data)

# for symbol in select_stock_n():
#     print(symbol)