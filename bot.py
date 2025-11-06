# src/bot.py
from config import Config
from ib_insync import IB, util, Contract, MarketOrder
import logging

log = logging.getLogger(__name__)

class IBWrapper:
    def __init__(self):
        self.config = Config
        self.ib = None
        self.connected = False

    def connect(self):
        if Config.TEST_MODE:
            log.info("TEST_MODE enabled: not connecting to IB.")
            self.connected = False
            return
        self.ib = IB()
        self.ib.connect(Config.IB_HOST, Config.IB_PORT, clientId=Config.IB_CLIENT_ID)
        self.connected = self.ib.isConnected()
        log.info(f"Connected to IB: {self.connected}")

    def disconnect(self):
        if self.ib and self.ib.isConnected():
            self.ib.disconnect()
            self.connected = False

    def make_crypto_contract(self, symbol="SOLUSD"):
        """
        Create a contract for crypto at IB.
        IB uses: symbol, secType='CRYPTO', exchange='PAXOS' or 'ZEROHASH' etc.
        Best practice: use ConId + Exchange in production. Here we build a simple contract.
        """
        # NOTE: exchange may differ per IB setup; user must confirm correct exchange for SOL on their account.
        return Contract(symbol=symbol, secType='CRYPTO', exchange='PAXOS', currency='USD')

    def place_market_order(self, contract, qty, action="BUY"):
        if Config.TEST_MODE:
            log.info(f"[TEST_MODE] Would place {action} market order for {qty} {contract.symbol}")
            return {"status":"simulated","action":action,"qty":qty,"symbol":contract.symbol}
        order = MarketOrder(action, qty)
        trade = self.ib.placeOrder(contract, order)
        return trade
