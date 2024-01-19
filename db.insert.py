import psycopg2
from psycopg2 import sql
import pandas as pd
# 建立資料庫連線
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
result = pd.read_csv("result.csv")
num_rows, num_columns = result.shape
for row in range(1,num_rows):
    stock_values = tuple(result.iloc[row,:].values)
    sql_query = f"insert into {table_name} values {stock_values}"
    cursor.execute(sql_query)

cursor.execute
# 提交變更
conn.commit()

# 關閉 cursor 和連線
cursor.close()
conn.close()
