import ccxt
from redis_cache import RedisCache

class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binance.vision/api',
                    'private': 'https://testnet.binance.vision/api',
                }
            }
        })
        self.exchange.set_sandbox_mode(True)
        self.cache = RedisCache()

    def get_ticker(self, symbol='BTC/USDT'):
        """Obtém o preço do cache ou da API, armazenando no Redis."""
        cache_key = f"ticker:{symbol}"
        cached_data = self.cache.get_data(cache_key)
        
        if cached_data:
            return cached_data
        
        ticker = self.exchange.fetch_ticker(symbol)
        data = {
            'symbol': ticker['symbol'],
            'last_price': ticker['last'],
            'timestamp': ticker['timestamp']
        }
        self.cache.set_data(cache_key, data)
        return data

    def get_balance(self):
        return self.exchange.fetch_balance()