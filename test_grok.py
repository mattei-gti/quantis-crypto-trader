from grok_client import GrokClient
from dotenv import load_dotenv
import os

load_dotenv()

# Dados fictícios para teste
price_data = {
    'last_price': 85840.94,
    'timestamp': 1742780477863
}

client = GrokClient()
signal = client.get_trading_signal('BTC/USDT', price_data)
print(f"Sinal da Grok: {signal}")