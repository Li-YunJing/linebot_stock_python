import psycopg2
from psycopg2 import sql
import pandas as pd
# 建立資料庫連線
def watch_list():
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
    
    output_string = ""

    if signal_data.empty:
            output_string += "今日無適當進出場時機，繼續持有等待時機!"
    else:    
        for index, row in signal_data.iterrows():
            output_string += f"股票代號: {row['symbol']}\n"
            output_string += f"Date: {row['date']}\n"
            output_string += f"關注: {row['action']}\n"
            output_string += "-------------------\n"

    cursor.execute
    # 提交變更
    conn.commit()

    # 關閉 cursor 和連線
    cursor.close()
    conn.close()
    return output_string