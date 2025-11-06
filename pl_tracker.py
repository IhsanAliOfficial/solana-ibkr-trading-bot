# pl_tracker.py
from ibkr_client import get_current_price
import pandas as pd

positions = pd.DataFrame(columns=["Symbol", "Action", "Quantity", "Price", "PL"])

def add_position(position):
    global positions
    positions = pd.concat([positions, pd.DataFrame([position])], ignore_index=True)

def update_pl():
    global positions
    for idx, row in positions.iterrows():
        current_price = get_current_price(row["Symbol"])
        if row["Action"] == "BUY":
            positions.at[idx, "PL"] = (current_price - row["Price"]) * row["Quantity"]
        else:
            positions.at[idx, "PL"] = (row["Price"] - current_price) * row["Quantity"]
    return positions
