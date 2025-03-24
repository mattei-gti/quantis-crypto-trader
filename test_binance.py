from binance_client import BinanceClient
from telegram_bot import TelegramBot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

client = BinanceClient(API_KEY, SECRET_KEY)
telegram = TelegramBot()

# Testa o preço e envia notificação
ticker = client.get_ticker('BTC/USDT')
print(f"Preço atual de {ticker['symbol']}: {ticker['last_price']} USDT")
message = f"Preço atual de {ticker['symbol']}: {ticker['last_price']} USDT"
asyncio.run(telegram.send_message(message))

# Testa o saldo
balance = client.get_balance()
print("Saldo da conta:", balance['total'])