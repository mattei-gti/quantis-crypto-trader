from binance_client import BinanceClient
from telegram_bot import TelegramBot
from grok_client import GrokClient
import asyncio
import time

class TradingLogic:
    def __init__(self, api_key, secret_key):
        self.client = BinanceClient(api_key, secret_key)
        self.telegram = TelegramBot()
        self.grok = GrokClient()
        self.symbol = 'BTC/USDT'

    async def monitor_and_trade(self):
        while True:
            ticker = self.client.get_ticker(self.symbol)
            price = ticker['last_price']
            balance = self.client.get_balance()['total']
            usdt_balance = balance.get('USDT', 0)
            btc_balance = balance.get('BTC', 0)

            message = f"Monitorando {self.symbol}: Preço atual = {price} USDT"
            print(message)
            await self.telegram.send_message(message)

            # Obtém sinal da Grok
            signal = self.grok.get_trading_signal(self.symbol, ticker)
            print(f"Sinal da Grok: {signal}")
            await self.telegram.send_message(f"Sinal da Grok: {signal}")

            # Executa trades com base no sinal
            if signal == 'buy' and usdt_balance > 10:
                amount = 0.001
                order = self.client.exchange.create_market_buy_order(self.symbol, amount)
                message = f"Compra executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                print(message)
                await self.telegram.send_message(message)

            elif signal == 'sell' and btc_balance >= 0.001:
                amount = 0.001
                order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                message = f"Venda executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                print(message)
                await self.telegram.send_message(message)

            time.sleep(60)  # Verifica a cada 60 segundos