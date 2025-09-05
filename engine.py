import ccxt
import os
import pandas as pd
import mplfinance as mpf
import io
import random
from dotenv import load_dotenv
from telegram_bot import send_telegram_message
from utils import get_top_symbols

load_dotenv()

exchange = ccxt.binance()
TIMEFRAME = os.getenv("TIMEFRAME", "15m")

def generate_signal(symbol, timeframe="15m"):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=50)
    last_close = ohlcv[-1][4]

    action = random.choice(["BUY", "SELL", "NO_TRADE"])
    confidence = random.randint(60, 95)

    entry_price = round(last_close, 2)
    tp = None
    if action == "BUY":
        tp = round(entry_price * 1.02, 2)
    elif action == "SELL":
        tp = round(entry_price * 0.98, 2)

    return {
        "action": action,
        "confidence": confidence,
        "entry": entry_price,
        "tp": tp,
        "ohlcv": ohlcv
    }

def format_message(symbol, signal, timeframe="15m"):
    msg = f"📊 {symbol} ({timeframe})\n" \
          f"Sinyal: {signal['action']}\n" \
          f"Confidence: {signal['confidence']}%\n" \
          f"Entry: {signal['entry']}"
    if signal['tp']:
        msg += f"\nTP: {signal['tp']}"
    return msg

def generate_chart(symbol, signal, timeframe="15m"):
    df = pd.DataFrame(signal["ohlcv"], columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Tambah EMA
    df["EMA20"] = df["close"].ewm(span=20).mean()

    buf = io.BytesIO()
    mpf.plot(df, type="candle", style="yahoo", volume=True,
             addplot=[mpf.make_addplot(df["EMA20"], color="blue")],
             savefig=buf)
    buf.seek(0)
    return buf

def main():
    symbols = get_top_symbols(20)
    for symbol in symbols:
        try:
            signal = generate_signal(symbol, timeframe=TIMEFRAME)
            msg = format_message(symbol, signal, timeframe=TIMEFRAME)
            chart = generate_chart(symbol, signal, timeframe=TIMEFRAME)
            send_telegram_message(msg, chart_buf=chart)
        except Exception as e:
            print(f"Error {symbol}: {e}")

if __name__ == "__main__":
    main()
