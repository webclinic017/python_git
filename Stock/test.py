import requests
import pandas as pd
from bs4 import BeautifulSoup

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1000)
pd.set_option('max_colwidth', 100)

url = "https://goodinfo.tw/StockInfo/StockList.asp?RPT_TIME=&MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT=%E5%96%AE%E6%9C%88%E7%87%9F%E6%94%B6%E5%B9%B4%E5%A2%9E%E7%8E%87%28%E6%9C%AC%E6%9C%88%E4%BB%BD%29%40%40%E5%96%AE%E6%9C%88%E7%87%9F%E6%94%B6%E5%B9%B4%E5%A2%9E%E6%B8%9B%E7%8E%87%40%40%E6%9C%AC%E6%9C%88%E4%BB%BD%E5%B9%B4%E5%A2%9E%E7%8E%87"

# url = "https://goodinfo.tw/StockInfo/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT2=DATE"
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
# print(df)
# print(df.iloc[6,2])
df.set_index("代號", inplace=True)
df.drop("代號", inplace=True)
# print(df)

df.reset_index(inplace=True)
print(df)
# print(df.shape[0])

for i in range(df.shape[0]-1, -1, -1):
	print(df.iloc[i,2].strip())
	print(i)
	if df.iloc[i,2].strip() != "⊕  ⊕  ⊕":
		print("find it")
		print(df.iloc[i,0].strip())
		index = df.iloc[i,0].index
		# print(index)
		# df.drop(df.iloc[i,0], inplace=True)
		df.drop(i, axis=0, inplace=True)
print(df)		