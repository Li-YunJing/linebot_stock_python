import psycopg2
from psycopg2 import sql

# 建立資料庫連線
conn = psycopg2.connect(
    host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
    user="stock_zs94_user",
    password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
    database="stock_zs94"   
)

# 建立一個 cursor 物件
cursor = conn.cursor()

table_name = "stockdb"

# 建立資料表
create_table_query = sql.SQL("""
    CREATE TABLE {} (
        stock_n VARCHAR(255),
        Date DATE,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        "Adj Close" FLOAT,
        Volume FLOAT,
        PRIMARY KEY (stock_n, Date)
    )
""").format(sql.Identifier(table_name))

# 執行 SQL 語句
cursor.execute(create_table_query)

# 提交變更
conn.commit()

# 關閉 cursor 和連線
cursor.close()
conn.close()


