import psycopg2
from psycopg2 import sql
import pandas as pd
# 建立資料庫連線
def signal_data():
    conn = psycopg2.connect(
        host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
        user="stock_zs94_user",
        password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
        database="stock_zs94"   
    )

    # 建立一個 cursor 物件
    cursor = conn.cursor()

    # 動態組合 SQL 查詢，使用 TO_CHAR 函數將日期格式化
    table_name = "signals"
    date_format = "YYYY-MM-DD"  # 你想要的日期格式
    sql_query = f"SELECT symbol, date, action FROM {table_name}"
    cursor.execute(sql_query)
    # 獲取所有結果
    signal_data = cursor.fetchall()
    signal_data = pd.DataFrame(signal_data)
    signal_data.columns = ['symbol', 'date', 'action']
    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()

    return signal_data
def watch_list():
    result = signal_data()
    if result.empty:
            print("今日無適當進出場時機，繼續持有等待時機!")
    else:    
        for index, row in result.iterrows():
            print(f"股票代號: {row['symbol']}")
            print(f"Date: {row['date']}")
            print(f"關注: {row['action']}")
            print("-------------------")
    return ""
