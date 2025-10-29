from backtesting import Backtest
from backtesting.test import GOOG
from backend.strategy import SmaCross

bt = Backtest(GOOG, SmaCross, cash=10000, commission=.002)
stats = bt.run()
print(stats)
bt.plot()
