from binance_client import BinanceClient
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém as chaves de API do ambiente
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

# Instancia o cliente
client = BinanceClient(API_KEY, SECRET_KEY)

# Testa a obtenção de preço
ticker = client.get_ticker('BTC/USDT')
print(f"Preço atual de {ticker['symbol']}: {ticker['last_price']} USDT")

# Testa o saldo
balance = client.get_balance()
print("Saldo da conta:", balance['total'])