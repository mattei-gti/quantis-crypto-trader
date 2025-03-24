import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')

    def get_trading_signal(self, symbol, price_data):
        """Simula um sinal de negociação."""
        price = price_data['last_price']
        if price < 85000:
            return 'buy'
        elif price > 85500:
            return 'sell'
        return 'hold'