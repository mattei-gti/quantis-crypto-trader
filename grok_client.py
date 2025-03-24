import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    def __init__(self):
        self.api_key = os.getenv('GROK_API_KEY')
        self.endpoint = 'https://grok-api-4zap.onrender.com/v1/grok'  # Endpoint oficial

    def get_trading_signal(self, symbol, price_data):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'symbol': symbol,
            'price': price_data['last_price'],
            'timestamp': price_data['timestamp'],
            'query': f"Analyze {symbol} at {price_data['last_price']} USDT. Should I buy, sell, or hold?"
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            signal = data.get('signal', 'hold')
            return signal.lower()
        except requests.exceptions.RequestException as e:
            print(f"Erro na API Grok: {str(e)}")
            return 'hold'