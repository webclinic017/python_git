import yfinance as yf
import pandas as pd
from talib import abstract
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import graphviz 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
import os

# os.environ['PATH'] += os.pathsep + 'C:\Users\amy50\Downloads\Graphviz\bin'

# 叫出一棵決策樹
model = DecisionTreeClassifier(max_depth = 7)

stk = yf.Ticker('SPY')
# 取得 2000 年至今的資料
data = stk.history(start = '2000-01-01')
# 簡化資料，只取開、高、低、收以及成交量
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

data.columns = ['open','high','low','close','volume']
# 隨意試試看這幾個因子好了
ta_list = ['MACD','RSI','MOM','STOCH']
# 快速計算與整理因子
for x in ta_list:
    output = eval('abstract.'+x+'(data)')
    output.name = x.lower() if type(output) == pd.core.series.Series else None
    data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
    data = data.set_index('key_0')
# print(data)    

# 五日後漲標記 1，反之標記 0
data['week_trend'] = np.where(data.close.shift(-5) > data.close, 1, 0)

# 檢查資料有無缺值
data.isnull().sum()
# 最簡單的作法是把有缺值的資料整列拿掉
data = data.dropna()
print(data)

# 決定切割比例為 70%:30%
split_point = int(len(data)*0.7)
# 切割成學習樣本以及測試樣本
train = data.iloc[:split_point,:].copy()
test = data.iloc[split_point:-5,:].copy()

# 訓練樣本再分成目標序列 y 以及因子矩陣 X
train_X = train.drop('week_trend', axis = 1)
train_y = train.week_trend
# 測試樣本再分成目標序列 y 以及因子矩陣 X
test_X = test.drop('week_trend', axis = 1)
test_y = test.week_trend

# 讓 A.I. 學習
model.fit(train_X, train_y)

# 讓 A.I. 測驗，prediction 存放了 A.I. 根據測試集做出的預測
prediction = model.predict(test_X)

dot_data = export_graphviz(model, out_file = None,
                           feature_names = train_X.columns,
                           filled = True, rounded = True,
                           class_names = True,
                           special_characters = True)
graph = graphviz.Source(dot_data)
graph.render('./round-table.gv', view=True)

# 混淆矩陣
confusion_matrix(test_y, prediction)
# 準確率
model.score(test_X, test_y)

# 計算 ROC 曲線
false_positive_rate, true_positive_rate, thresholds = roc_curve(test_y, prediction)

# 計算 AUC 面積
print(auc(false_positive_rate, true_positive_rate))

# 測試一批深度參數，一般而言深度不太會超過 3x，我們這邊示範 1 到 50 好了
depth_parameters = np.arange(1, 50)
# 準備兩個容器，一個裝所有參數下的訓練階段 AUC；另一個裝所有參數下的測試階段 AUC
train_auc= []
test_auc = []
# 根據每一個參數跑迴圈
for test_depth in depth_parameters:
    # 根據該深度參數，創立一個決策樹模型，取名 temp_model
    temp_model = DecisionTreeClassifier(max_depth = test_depth)
    # 讓 temp_model 根據 train 學習樣本進行學習
    temp_model.fit(train_X, train_y)
    # 讓學習後的 temp_model 分別根據 train 學習樣本以及 test 測試樣本進行測驗
    train_predictions = temp_model.predict(train_X)
    test_predictions = temp_model.predict(test_X)
    # 計算學習樣本的 AUC，並且紀錄起來
    false_positive_rate, true_positive_rate, thresholds = roc_curve(train_y, train_predictions)
    auc_area = auc(false_positive_rate, true_positive_rate)
    train_auc.append(auc_area)
    # 計算測試樣本的 AUC，並且紀錄起來
    false_positive_rate, true_positive_rate, thresholds = roc_curve(test_y, test_predictions)
    auc_area = auc(false_positive_rate, true_positive_rate)
    test_auc.append(auc_area)

# 繪圖視覺化
plt.figure(figsize = (14,10))
plt.plot(depth_parameters, train_auc, 'b', label = 'Train AUC')
plt.plot(depth_parameters, test_auc, 'r', label = 'Test AUC')
plt.ylabel('AUC')
plt.xlabel('depth parameter')
plt.show()

# test 是我們在切割樣本的時候，切出來的測試樣本，包含了價量資訊，我們首先將 A.I. 在這期間的預測結果 prediction 放進去
test['prediction'] = prediction

# 這次的二元分類問題很單純，若直接把 prediction 位移一天，剛好就會是模擬買賣的狀況：
# T-1 日的預測為「跌」而 T 日的預測為「漲」，則 T+1 日開盤『買進』
# T-1 日的預測為「漲」而 T 日的預測為「跌」，則 T+1 日開盤『賣出』
# 連續預測「漲」，則『持續持有』
# 連續預測「跌」，則『空手等待』
test['status'] = test.prediction.shift(1).fillna(0)

# 所以什麼時候要買股票就很好找了：status 從 0 變成 1 的時候，1 的那天的開盤買進（因為 status 已經位移一天了喔）
# 從 prediction 的角度解釋就是：當 A.I. 的預測從 0 變成 1 的時候，1 的隔天的開盤買進
test['buy_cost'] = test.open[np.where((test.status == 1)&(test.status.shift(1) == 0))[0]]
# 同理，賣股票也很好找：status 從 1 變成 0 的時候，0 的那天的開盤賣出
test['sell_cost'] = test.open[np.where((test.status == 0)&(test.status.shift(1) == 1))[0]]
# 把缺值補上 0
test = test.fillna(0)

# 來算算每次買賣的報酬率吧！
# 一買一賣是剛好對應的，所以把買的成本以及賣的價格這兩欄的數字取出，就能輕易的算出交易報酬率

buy_cost = np.array(test.buy_cost[test.buy_cost != 0])
sell_price = np.array(test.sell_cost[test.sell_cost != 0])

# # 但是回測的最後一天，有時候會發現還有持股尚未賣出喔！由於還沒賣就不能當作一次完整的交易，
# 所以最後一次的買進，我們先忽略
if len(buy_cost) > len(sell_price) :
    buy_cost = buy_cost[:-1]

trade_return = sell_price / buy_cost - 1

# 交易都會有交易成本，例如台股每次一買一賣約產生 0.6% 的交易成本。
# 買賣 SPY ETF 也會有交易成本，管理費用約 0.1%，券商手續費因人而異，但近年來此費用逐漸趨近於 0，這裡就假設 0.1% 手續費好了
# 因此這裡額外計算一個把每次交易報酬率扣除總交易成本約 0.2% 的淨報酬率
fee = 0.002
net_trade_return = trade_return - fee

# 把報酬率都放進表格吧！
test['trade_ret'] = 0
test['net_trade_ret'] = 0
sell_dates = test.sell_cost[test.sell_cost != 0].index
test.loc[sell_dates, 'trade_ret'] = trade_return
test.loc[sell_dates, 'net_trade_ret'] = net_trade_return

# 如果還想要畫出績效走勢圖，那就要把策略的報酬率也算出來，由於我們不論買賣都是以開盤價進行，所以策略的報酬率會使用開盤價計算
test['open_ret'] = test.open / test.open.shift(1) - 1
test['strategy_ret'] = test.status.shift(1) * test.open_ret
test['strategy_net_ret'] = test.strategy_ret
test.loc[sell_dates, 'strategy_net_ret'] = test.loc[sell_dates, 'strategy_net_ret'] - fee
test = test.fillna(0)

# 計算出績效走勢圖
test['buy_and_hold_equity'] = (test.open_ret + 1).cumprod()
test['strategy_equity'] = (test.strategy_ret + 1).cumprod()
test['strategy_net_equity'] = (test.strategy_net_ret + 1).cumprod()

# 計算出一些有用的策略績效數字吧！
trade_count = len(sell_dates)
trade_count_per_year = trade_count / (len(test)/252)
win_rate = (net_trade_return > 0).sum() / trade_count
profit_factor = net_trade_return[net_trade_return > 0].sum() / abs(net_trade_return[net_trade_return < 0].sum())
mean_net_return = np.mean(net_trade_return)
acc_ret = test.strategy_net_equity[-1] - 1
strategy_ear = test.strategy_net_equity[-1] ** (252/len(test)) - 1
strategy_std = test.strategy_net_ret.std() * (252**0.5)
strategy_sharpe = (strategy_ear - 0.01) / strategy_std

# 也畫出績效走勢看看吧！
image = test.buy_and_hold_equity.plot()
image = test.strategy_equity.plot()
image = test.strategy_net_equity.plot()

fig = image.get_figure()                      #取得圖片
fig.savefig('./figure.png')                     #保存成png
fig.savefig('./figure.pdf')  

