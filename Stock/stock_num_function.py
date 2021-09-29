import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('max_colwidth', 100)


def yoy():
	start = time.time()
	url = "https://goodinfo.tw/StockInfo/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%96%AE%E6%9C%88%E7%87%9F%E6%94%B6%E5%B9%B4%E5%A2%9E%E7%8E%87%28%E6%9C%AC%E6%9C%88%E4%BB%BD%29%40%40%E5%96%AE%E6%9C%88%E7%87%9F%E6%94%B6%E5%B9%B4%E5%A2%9E%E6%B8%9B%E7%8E%87%40%40%E6%9C%AC%E6%9C%88%E4%BB%BD%E5%B9%B4%E5%A2%9E%E7%8E%87"

	headers = {
		"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36"
	}
	response = requests.get(url, headers=headers)
	response.encoding = "utf-8"

	# print(response.text)
	soup = BeautifulSoup(response.text, 'lxml')
	data = soup.select_one("#divStockList").prettify()
	df = pd.read_html(data)[0]

	df = df[["代號", "名稱", "月營收  增減  註記"]]
	df.set_index("代號", inplace=True)
	df.drop("代號", inplace=True)

	df.reset_index(inplace=True)

	good_list = []
	for i in range(df.shape[0]-1, -1, -1):
		if df.iloc[i,2].strip() == "⊕  ⊕  ⊕":
			good_list.append(df.iloc[i,0])
	# print(df)		
	# print(good_list)
	end = time.time()
	delta = end-start
	print("program time: " + str(delta))
	print("======================================find_goodYoY end======================================")
	return good_list

def All_sotck():
	start = time.time()
	url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
	response = requests.get(url)
	listed = pd.read_html(response.text)[0]
	listed.columns = listed.iloc[0,:]
	stock_1 = listed[["有價證券代號"]]
	all_stock_list = []
	for i in range(0, stock_1.shape[0], 1):
		all_stock_list.append(stock_1.iloc[i,0])		
	# print(all_stock_list)	
	end = time.time()
	delta = end-start
	print("program time: " + str(delta))
	print("======================================find_All stock end======================================")
	return all_stock_list
# yoy()	
# All_sotck()