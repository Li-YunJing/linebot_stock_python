def  latestdate():
    import psycopg2
    from psycopg2 import sql
    import datetime

    # 連接到 PostgreSQL 資料庫
    conn = psycopg2.connect(
        host="dpg-cmj1eaol5elc73ep9u0g-a.singapore-postgres.render.com",
        user="stock_zs94_user",
        password="R8YZugNEL8DbqkNAUmw7NLyezRKGyvT8",
        database="stock_zs94"   
    )

    cursor = conn.cursor()

    # 欲查詢的目標日期
    target_date = datetime.date.today()

    # 撈取最接近目標日期的一筆資料
    query = sql.SQL("SELECT * FROM stockdb ORDER BY ABS(date - %s) LIMIT 1;")
    cursor.execute(query, (target_date,))
    result = cursor.fetchone()
    # 處理查詢結果，result 包含最接近日期的資料

    # 關閉資料庫連線
    cursor.close()
    conn.close()
    
    return result[1]