import requests
import pandas as pd
from io import StringIO
import datetime
import os
import time
from bs4 import BeautifulSoup
import backtrader as bt
import backtrader.feeds as btfeeds
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select

stock_num = str(2330)
start = time.time()
driver = webdriver.Firefox()
driver.get("https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID=" + stock_num + "&CHT_CAT2=DATE") 
select = Select(driver.find_element_by_id("selK_ChartPeriod"))
select.select_by_value("365") 
time.sleep(3)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('max_colwidth', 100)

try:
    os.remove("C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\dataFeed\\" + stock_num + ".csv")
except OSError as e:
    print(e)
else:
    print("================================File is deleted successfully================================")

sourceFile = open("C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\dataFeed\\page_source.txt", "w", encoding='utf-8')
# # pattern_date = r'\d*'
# # start = time.time()
# # url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
# # response = requests.get(url)
# # listed = pd.read_html(response.text)
# # # print(listed)
# # # print(listed[0])
# # # listed.columns = listed.iloc[0,:]
# # # print(listed)
# # listed = pd.read_html(response.text)[0]
# # print(type(listed))
# # print(listed.shape)
# # print(listed.columns)
# # print(listed.iloc[0,:])
# # listed.columns = listed.iloc[0,:]
# # listed = listed[["有價證券代號","有價證券名稱","市場別","產業別","公開發行/上市(櫃)/發行日"]]
# # # listed = listed.iloc[1:]
# # print(listed.iloc[1:])
# # # listed = listed.iloc[0:]
# # print(listed.iloc[0:])
# # stock_1 = listed["有價證券代號"]
# # stock_num = stock_1.apply(lambda x: str(x) + ".TW")
# # print(stock_num)

# url = "https://query1.finance.yahoo.com/v7/finance/download/" + stock_id + "?period1=" + str(s1) + "&amp;period2=" + str(s2) + "&amp;interval=1d&amp;events=history&amp;includeAdjustedClose=true"
url_tmp = driver.page_source
print(url_tmp, file=sourceFile)
sourceFile.close()
# url = "https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT2=DATE"
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
# }
# response = requests.get(url, headers=headers)
# response.encoding = "utf-8"
# print(response.text)

soup = BeautifulSoup(driver.page_source, 'lxml')
data = soup.select_one("#divPriceDetail").prettify()
df = pd.read_html(data)[0]
df.columns = df.columns.get_level_values(1)
df = df[["交易  日期", "開盤", "最高", "最低", "收盤", "張數"]]
df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

print(df.iloc[1,0])
str_year = "2021-"
for i in range(0, df.shape[0], 1):
    if str_year == "2021-":
        if (df.iloc[i,0].split("/")[0] == "01" and df.iloc[i+1,0].split("/")[0] == "12"):
            df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")
            str_year = "2020-"
            continue
        df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")
    else:
         df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")   

df.set_index("Date", inplace=True)
  
df.drop("2021-交易  日期", inplace=True)
df.drop("2020-交易  日期", inplace=True)

print(df) 
df.sort_index(inplace=True)
df.to_csv("C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\dataFeed\\" + stock_num + ".csv", encoding='utf-8')

end = time.time()
delta = end - start
driver.quit()
print("Program time: " + str(delta))