# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TEST_MODE = os.getenv("TEST_MODE", "0") in ("0", "true", "True")
    IB_HOST = os.getenv("IB_HOST", "127.0.0.1")
    IB_PORT = int(os.getenv("IB_PORT", "7497"))
    IB_CLIENT_ID = int(os.getenv("IB_CLIENT_ID", "123"))
    DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "SOLUSD")
    ORDER_QTY = float(os.getenv("ORDER_QUANTITY", "1"))
