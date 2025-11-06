# src/main.py
import PySimpleGUI as sg
import threading
import time
from config import Config
from bot import IBWrapper
from strategy import SMACrossoverStrategy
from utils import generate_fake_market_data
import pandas as pd

sg.theme('DarkBlue')

ibw = IBWrapper()
strategy = SMACrossoverStrategy(short=5, long=20)
df = generate_fake_market_data(minutes=300, start_price=20.0)  # initial simulated data

layout = [
    [sg.Text('Solana (SOL) IBKR Test Bot', font=('Any', 16))],
    [sg.Text('Mode:'), sg.Text('TEST' if Config.TEST_MODE else 'LIVE', key='-MODE-')],
    [sg.Text('Latest Price:'), sg.Text('', key='-PRICE-')],
    [sg.Button('Start'), sg.Button('Stop'), sg.Button('Place Sim Buy'), sg.Button('Place Sim Sell')],
    [sg.Multiline('', size=(80,10), key='-LOG-')]
]

window = sg.Window('SOL IBKR Bot', layout, finalize=True)

running = False

def log(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    window['-LOG-'].print(f"[{now}] {msg}")

def run_loop():
    global df, running
    ibw.connect()
    log("Bot started (TEST_MODE={})".format(Config.TEST_MODE))
    while running:
        # In TEST mode: append a new fake price point
        if Config.TEST_MODE:
            new = generate_fake_market_data(minutes=1, start_price=df['close'].iloc[-1])
            df = pd.concat([df, new.tail(1)])
        # Evaluate strategy
        sig = strategy.generate_signal(df)
        price = df['close'].iloc[-1]
        window['-PRICE-'].update(f"{price:.4f}")
        if sig == 'buy':
            log("Strategy signal: BUY")
            resp = ibw.place_market_order(ibw.make_crypto_contract(Config.DEFAULT_SYMBOL), Config.ORDER_QTY, action='BUY')
            log(f"Order result: {resp}")
        elif sig == 'sell':
            log("Strategy signal: SELL")
            resp = ibw.place_market_order(ibw.make_crypto_contract(Config.DEFAULT_SYMBOL), Config.ORDER_QTY, action='SELL')
            log(f"Order result: {resp}")
        time.sleep(1)  # wait 1s between iterations

# Event loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WINDOW_CLOSED:
        running = False
        break
    if event == 'Start' and not running:
        running = True
        t = threading.Thread(target=run_loop, daemon=True)
        t.start()
    if event == 'Stop':
        running = False
        ibw.disconnect()
        log("Bot stopped")
    if event == 'Place Sim Buy':
        resp = ibw.place_market_order(ibw.make_crypto_contract(Config.DEFAULT_SYMBOL), Config.ORDER_QTY, action='BUY')
        log(f"Manual BUY: {resp}")
    if event == 'Place Sim Sell':
        resp = ibw.place_market_order(ibw.make_crypto_contract(Config.DEFAULT_SYMBOL), Config.ORDER_QTY, action='SELL')
        log(f"Manual SELL: {resp}")

window.close()
