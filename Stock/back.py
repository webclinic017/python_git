# data feeds
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import math

# 從Yahoo Finance取得資料
# data = btfeeds.YahooFinanceData(dataname='TESLA', 
#                                 fromdate=datetime.datetime(2019, 1, 1),
#                                 todate=datetime.datetime(2019, 12, 31))

# data = bt.feeds.GenericCSVData(dataname='C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\2330.TW.csv') 
dt_start = datetime.datetime.strptime("20210721", "%Y%m%d")
dt_end = datetime.datetime.strptime("20210923", "%Y%m%d")


# class MyCsvFileData(bt.feeds.GenericCSVData):
#     # 自定义的文件格式
#     params = (
#         ('fromdate', datetime.datetime(2000, 1, 1)),
#         ('todate', datetime.datetime(2000, 12, 31)),
#         ('nullvalue', 0.0),
#         ('dtformat', ('%Y-%m-%d %H:%M:%S')),
#         # ('tmformat', ('%H.%M.%S')),
#         ('nullvalue', 0.00),
#         ('datetime', 0),
#         ('high', 1),
#         ('low', 2),
#         ('open', 3),
#         ('close', 4),
#         ('volume', 'vol'),
#         ('openinterest', -1)
#     )
# data = MyCsvFileData(dataname='C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\2330.TW.csv', start="20001219", end="20001225")
data = bt.feeds.GenericCSVData(
    dataname='C:\\Users\\Brian.tsai\\Desktop\\Python\\Stock\\20210924.csv',
    fromdate=dt_start,      # 起止日期
    todate=dt_end,
    nullvalue=0.0,
    dtformat=('%Y-%m-%d'),  # 日期列的格式
    datetime=0,             # 各列的位置，从0开始，如列缺失则为None，-1表示自动根据列名判断
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1
)

# sma cross strategy
class SmaCross(bt.Strategy):
    # 交易紀錄
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    # 設定交易參數
    params = dict(
        ma_period_short=5,
        ma_period_long=10
    )

    def __init__(self):
        # 均線交叉策略
        sma1 = bt.ind.SMA(period=self.p.ma_period_short)
        sma2 = bt.ind.SMA(period=self.p.ma_period_long)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        
        # 使用自訂的sizer函數，將帳上的錢all-in
        self.setsizer(sizer())
        
        # 用開盤價做交易
        self.dataopen = self.datas[0].open

    def next(self):
        # 帳戶沒有部位
        if not self.position:
            # 5ma往上穿越20ma
            if self.crossover > 0:
                # 印出買賣日期與價位
                self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                # 使用開盤價買入標的
                self.buy(price=self.dataopen[0])
        # 5ma往下穿越20ma
        elif self.crossover < 0:
            # 印出買賣日期與價位
            self.log('SELL ' + ', Price: ' + str(self.dataopen[0]))
            # 使用開盤價賣出標的
            self.close(price=self.dataopen[0])

# 計算交易部位
class sizer(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return math.floor(cash/data[1])
        else:
            return self.broker.getposition(data)

# 初始化cerebro
cerebro = bt.Cerebro()
# feed data
cerebro.adddata(data)
# add strategy
cerebro.addstrategy(SmaCross)
# run backtest
cerebro.run()
# plot diagram
cerebro.plot()