import ccxt

class BinanceClient:
    def __init__(self, api_key, secret_key):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,  # Respeita limites de chamadas
            'options': {
                'defaultType': 'spot'  # Negociação à vista
            },
            'urls': {
                'api': {
                    'public': 'https://testnet.binance.vision/api',
                    'private': 'https://testnet.binance.vision/api',
                }
            }
        })
        # Forçar Testnet explicitamente
        self.exchange.set_sandbox_mode(True)

    def get_ticker(self, symbol='BTC/USDT'):
        ticker = self.exchange.fetch_ticker(symbol)
        return {
            'symbol': ticker['symbol'],
            'last_price': ticker['last'],
            'timestamp': ticker['timestamp']
        }

    def get_balance(self):
        return self.exchange.fetch_balance()