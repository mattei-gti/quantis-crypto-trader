from binance_client import BinanceClient

# Substitua pelas suas chaves da Binance Testnet
API_KEY = 'B1skBr4z6U5iwa9MlL1RFgITFvitpKs5rnVoF9rAVtnHtVVdOUQP3urWqKW2tvk6'
SECRET_KEY = '0zizt1fCpapxCY7LGcuzkwMTuOXlwQDH5YTDgebXIeMQpHR2fkWuHR2pqzvai89h'

# Instancia o cliente
client = BinanceClient(API_KEY, SECRET_KEY)

# Testa a obtenção de preço
ticker = client.get_ticker('BTC/USDT')
print(f"Preço atual de {ticker['symbol']}: {ticker['last_price']} USDT")

# Testa o saldo (opcional)
balance = client.get_balance()
print("Saldo da conta:", balance['total'])