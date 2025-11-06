# src/strategy.py
import pandas as pd

def sma(series, window):
    return series.rolling(window=window).mean()

class SMACrossoverStrategy:
    def __init__(self, short=5, long=20):
        self.short = short
        self.long = long
        self.position = 0  # 0 = flat, 1 = long

    def generate_signal(self, df):
        """
        df: DataFrame with 'close' column indexed by datetime.
        returns: 'buy'/'sell'/None
        """
        close = df['close']
        if len(close) < self.long:
            return None
        s = sma(close, self.short)
        l = sma(close, self.long)
        if s.iloc[-2] <= l.iloc[-2] and s.iloc[-1] > l.iloc[-1]:
            return 'buy'
        if s.iloc[-2] >= l.iloc[-2] and s.iloc[-1] < l.iloc[-1]:
            return 'sell'
        return None
