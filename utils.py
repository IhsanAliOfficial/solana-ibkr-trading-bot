# src/utils.py
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_fake_market_data(minutes=300, start_price=20.0):
    """
    Return a pandas DataFrame with datetime index and columns ['open','high','low','close','volume']
    Simple geometric-random-walk for testing.
    """
    timestamps = [datetime.now() - timedelta(minutes=minutes-i) for i in range(minutes)]
    prices = [start_price]
    for _ in range(1, minutes):
        change = random.gauss(0, 0.25)  # small noise
        prices.append(max(0.1, prices[-1] + change))
    df = pd.DataFrame({
        "datetime": timestamps,
        "open": prices,
        "high": [p + abs(random.gauss(0,0.2)) for p in prices],
        "low": [p - abs(random.gauss(0,0.2)) for p in prices],
        "close": prices,
        "volume": np.random.randint(100,1000, size=len(prices))
    }).set_index("datetime")
    return df
