from flask import Flask
import threading
import time
from engine import main

app = Flask(__name__)

# Jalankan bot loop di thread terpisah
def run_bot():
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)  # tunggu 5 menit sebelum scan ulang

@app.route("/")
def home():
    return "Crypto Bot is running on Render!"

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000)
