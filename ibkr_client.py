# ibkr_client.py
from ib_insync import IB, MarketOrder, Crypto
import config

ib = IB()
ib.connect(config.IBKR_HOST, config.IBKR_PORT, clientId=config.IBKR_CLIENT_ID)

def execute_trade(action, symbol=config.TRADING_SYMBOL, quantity=config.QUANTITY):
    contract = Crypto(symbol, 'PAXOS')  # IBKR crypto symbol
    ib.qualifyContracts(contract)
    price = ib.reqMktData(contract, '', False, False).last
    order = MarketOrder(action, quantity)
    trade = ib.placeOrder(contract, order)
    return {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "price": price
    }

def get_current_price(symbol=config.TRADING_SYMBOL):
    contract = Crypto(symbol, 'PAXOS')
    ib.qualifyContracts(contract)
    return ib.reqMktData(contract, '', False, False).last
