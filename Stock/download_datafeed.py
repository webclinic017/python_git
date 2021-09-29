import requests
import pandas as pd
from io import StringIO
import os
import time
from bs4 import BeautifulSoup
import backtrader as bt
import backtrader.feeds as btfeeds
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from stock_num_function import yoy
import random
import os

stock_list = yoy()
print(stock_list)
relative_path = os.getcwd()
start = time.time()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('max_colwidth', 100)
# stock_list = ["6712"]
for num in stock_list:
    print("current stock number: " + num)
    driver = webdriver.Firefox()
    driver.get("https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID=" + num + "&CHT_CAT2=DATE") 
    select = Select(driver.find_element_by_id("selK_ChartPeriod"))
    select.select_by_value("365") 

    delay_choices = [60, 61, 62, 63]  #延遲的秒數
    # delay_choices = [5]
    delay = random.choice(delay_choices)  #隨機選取秒數
    time.sleep(delay)  #延遲

    # time.sleep(3)

    try:
        os.remove(relative_path + "\\dataFeed\\" + num + ".csv")
    except OSError as e:
        print(e)
    else:
        print("================================File is deleted successfully================================")

    sourceFile = open(relative_path + "\\dataFeed\\page_source" + num + ".txt", "w", encoding='utf-8')

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

    # print(df.iloc[1,0])
    # print(df)
    str_year = "2021-"
    # print(df.shape[0])
    for i in range(0, df.shape[0], 1):
        # print(i)
        # print(df.iloc[i,0])
        if str_year == "2021-":
            try:
                if (df.iloc[i,0].split("/")[0] == "01" and df.iloc[i+1,0].split("/")[0] == "12"):
                    df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")
                    str_year = "2020-"
                    continue
                # print(df.iloc[i,0])
                df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")
            except IndexError as e:
                df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")
                print(e)
                print("No more data")
        else:
            df.iloc[i,0] = str_year + df.iloc[i,0].replace("/", "-")   

    df.set_index("Date", inplace=True)
    
    try:
        df.drop("2021-交易  日期", inplace=True)
        df.drop("2020-交易  日期", inplace=True)
    except KeyError as e:
        print(e)

    for i in range(0, df.shape[0], 1):
        # print(df.iloc[i,4])
        df.iloc[i,4] = float(df.iloc[i,4])*1000  #將張數轉成股數
    # print(df) 
    df.sort_index(inplace=True)
    df.to_csv(relative_path + "\\dataFeed\\" + num + ".csv", encoding='utf-8')

    driver.quit()

end = time.time()
delta = end - start
print("Program time: " + str(delta))
