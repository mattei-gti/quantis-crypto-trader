from binance_client import BinanceClient
from telegram_bot import TelegramBot
import asyncio
import time

class TradingLogic:
    def __init__(self, api_key, secret_key):
        self.client = BinanceClient(api_key, secret_key)
        self.telegram = TelegramBot()
        self.symbol = 'BTC/USDT'
        self.buy_threshold = 85622  # Comprar se o preço cair abaixo disso
        self.sell_threshold = 85800  # Vender se o preço subir acima disso

    async def monitor_and_trade(self):
        """Monitora o preço e executa trades com base em limites."""
        while True:
            ticker = self.client.get_ticker(self.symbol)
            price = ticker['last_price']
            balance = self.client.get_balance()['total']
            usdt_balance = balance.get('USDT', 0)
            btc_balance = balance.get('BTC', 0)

            message = f"Monitorando {self.symbol}: Preço atual = {price} USDT"
            print(message)
            await self.telegram.send_message(message)

            # Lógica de compra
            if price < self.buy_threshold and usdt_balance > 10:
                amount = 0.001  # Comprar 0.001 BTC (exemplo pequeno para Testnet)
                order = self.client.exchange.create_market_buy_order(self.symbol, amount)
                message = f"Compra executada: {amount} BTC a {price} USDT"
                print(message)
                await self.telegram.send_message(message)

            # Lógica de venda
            elif price > self.sell_threshold and btc_balance >= 0.001:
                amount = 0.001  # Vender 0.001 BTC
                order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                message = f"Venda executada: {amount} BTC a {price} USDT"
                print(message)
                await self.telegram.send_message(message)

            time.sleep(60)  # Verifica a cada 60 segundos