# Telegram Trading Signal Bot

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy config:
   ```bash
   cp .env.template .env
   ```
   Edit token, chat_id, symbol, timeframe.
3. Jalankan bot:
   ```bash
   python bot.py
   ```

Bot akan kirim sinyal setiap 15 menit, atau manual dengan perintah:
- `/start`
- `/status`
- `/signal`