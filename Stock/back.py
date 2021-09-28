import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import math
import os

relative_path = os.getcwd()
dt_start = datetime.datetime.strptime("20201021", "%Y%m%d")
dt_end = datetime.datetime.strptime("20210923", "%Y%m%d")
stock_num = "2611"
start_cash = 100000

try:
    os.remove(relative_path + "\\message.txt")
except OSError as e:
    print(e)
else:
    print("================================File is deleted successfully================================")

sourceFile = open(relative_path + "\\message.txt", "w", encoding='utf-8')

data = bt.feeds.GenericCSVData(
    dataname= relative_path + "\\dataFeed\\" + stock_num + ".csv",
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
        self.lines.top = bt.indicators.BollingerBands(self.datas[0], period=20).top
        self.lines.bot = bt.indicators.BollingerBands(self.datas[0], period=20).bot
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        
        # 使用自訂的sizer函數，將帳上的錢all-in
        self.setsizer(sizer())
        
        # 用開盤價做交易
        self.dataopen = self.datas[0].open

        # 關盤價
        self.dataclose = self.datas[0].close

        # 成交量
        self.datavolume = self.datas[0].volume

    def next(self):
        # print('當前可用資金', self.broker.getcash())
        print('當前可用資金', self.broker.getcash(), file=sourceFile)
        # print('當前總資產', self.broker.getvalue())
        print('當前總資產', self.broker.getvalue(), file=sourceFile)
        # print('當前持倉量', self.broker.getposition(self.data).size)
        print('當前持倉量', self.broker.getposition(self.data).size, file=sourceFile)
        # print('當前持倉成本', self.broker.getposition(self.data).price)
        print('當前持倉成本', self.broker.getposition(self.data).price, file=sourceFile)
        print(self.position, file=sourceFile)
        # 帳戶沒有部位
        if not self.position:
            # 5ma往上穿越20ma
            # print("bool top: " + str(self.lines.top[0]))
            # print("bool bot: " + str(self.lines.bot[0]))
            if self.crossover > 0 and self.dataclose[0] < 1.3 * self.lines.bot[0] : 

                # print("close: " + str(self.dataclose[0]))
                # print("bool: " + str(1.3 * self.lines.bot[0]))
                # 印出買賣日期與價位
                self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                # print("Volume: " + str(self.datavolume[0]))
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
            # print(data[0])
            # print(data[1])
            # print(math.floor(cash/data[0]))
            # print(math.floor(cash/data[1]))
            print("position___ : " + str(self.broker.getposition(data)))
            print("position___ : " + str(self.broker.getposition(data)), file=sourceFile)
            size = math.floor(cash/data[0])
            if size > 10:
                size = 10
            return size
        else:
            print("sell: " + str(self.broker.getposition(data)))
            return self.broker.getposition(data)

# 初始化cerebro
cerebro = bt.Cerebro()
# feed data
cerebro.adddata(data)
# add strategy
cerebro.addstrategy(SmaCross)

cerebro.broker.setcash(start_cash)
# cerebro.broker.setcommission(commission=0.002)

# run backtest
cerebro.run()

sourceFile.close()
# plot diagram
cerebro.plot()

