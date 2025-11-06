# tradingview.py
from flask import Flask, request

app = Flask(__name__)
signal_queue = []

@app.route('/signal', methods=['POST'])
def receive_signal():
    data = request.json
    signal = data.get('signal')
    if signal in ["BUY", "SELL"]:
        signal_queue.append(signal)
        return {"status": "received", "signal": signal}, 200
    return {"status": "error"}, 400

def get_signal():
    if signal_queue:
        return signal_queue.pop(0)
    return None

if __name__ == "__main__":
    app.run(port=5000)
