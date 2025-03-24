from binance_client import BinanceClient
from telegram_bot import TelegramBot
from grok_client import GrokClient
import asyncio
import time
import logging

# Configura logging
logging.basicConfig(
    filename='qct.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TradingLogic:
    def __init__(self, api_key, secret_key):
        self.client = BinanceClient(api_key, secret_key)
        self.telegram = TelegramBot()
        self.grok = GrokClient()
        self.symbol = 'BTC/USDT'
        self.stop_loss = 84000  # Vender se o preço cair abaixo disso
        self.last_buy_price = None  # Para rastrear o preço de compra

    async def monitor_and_trade(self):
        while True:
            try:
                ticker = self.client.get_ticker(self.symbol)
                price = ticker['last_price']
                balance = self.client.get_balance()['total']
                usdt_balance = balance.get('USDT', 0)
                btc_balance = balance.get('BTC', 0)

                message = f"Monitorando {self.symbol}: Preço atual = {price} USDT"
                print(message)
                logging.info(message)
                await self.telegram.send_message(message)

                # Obtém sinal da Grok
                signal = self.grok.get_trading_signal(self.symbol, ticker)
                message = f"Sinal da Grok: {signal}"
                print(message)
                logging.info(message)
                await self.telegram.send_message(message)

                # Lógica de compra
                if signal == 'buy' and usdt_balance > 10:
                    amount = 0.001
                    order = self.client.exchange.create_market_buy_order(self.symbol, amount)
                    self.last_buy_price = price
                    message = f"Compra executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)

                # Lógica de venda
                elif signal == 'sell' and btc_balance >= 0.001:
                    amount = 0.001
                    order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                    message = f"Venda executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)
                    self.last_buy_price = None

                # Stop-Loss
                elif self.last_buy_price and price < self.stop_loss and btc_balance >= 0.001:
                    amount = 0.001
                    order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                    message = f"Stop-Loss acionado: Vendido {amount} BTC a {price} USDT (Compra em {self.last_buy_price})"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)
                    self.last_buy_price = None

                time.sleep(60)  # Verifica a cada 60 segundos

            except Exception as e:
                error_message = f"Erro no monitoramento: {str(e)}"
                print(error_message)
                logging.error(error_message)
                await self.telegram.send_message(error_message)
                time.sleep(60)  # Continua após erro