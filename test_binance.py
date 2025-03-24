from binance_client import BinanceClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

client = BinanceClient(API_KEY, SECRET_KEY)

# Testa o preço com cache
for _ in range(2):  # Executa duas vezes para testar cache
    ticker = client.get_ticker('BTC/USDT')
    print(f"Preço atual de {ticker['symbol']}: {ticker['last_price']} USDT")

# Testa o saldo
balance = client.get_balance()
print("Saldo da conta:", balance['total'])