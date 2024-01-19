# 個股資訊

import requests
from bs4 import BeautifulSoup

def stock_id(message):
    try:
        url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(message)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        res = requests.get(url,headers = headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        soup1 = soup.find("table",{"class":"b1 p4_2 r10 box_shadow"})
        soup_stock_data = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
        soup2 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
        soup_stock_name = soup2.find("a").text.split("\xa0")
        soup3 = soup.find("table",{"class":"b1 p4_4 r10 box_shadow"})
        soup_stock_info = soup3.find_all("td",{"bgcolor":"white"})
        mes = "股票代號 :{} \n股票名稱 : {} \n產業別 : {} \n市場 : {}\n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {} \n資本額 : {} \n市值 : {}".format(soup_stock_name[0], soup_stock_name[1], soup_stock_info[1].text, soup_stock_info[2].text, soup_stock_data[0], soup_stock_data[1], soup_stock_data[2], soup_stock_data[3], soup_stock_data[4], soup_stock_data[5],soup_stock_data[6],soup_stock_data[7], soup_stock_info[4].text, soup_stock_info[5].text)
        return mes
    except:
        return "正確輸入方式為\n(ex.個股資訊 2330 / 個股資訊 台積電)"
