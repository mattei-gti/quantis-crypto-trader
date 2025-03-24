from binance_client import BinanceClient
from telegram_bot import TelegramBot
from grok_client import GrokClient
import asyncio
import time
import logging

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
        self.stop_loss = 84000
        self.last_buy_price = None
        self.last_check_time = 0
        self.check_interval = 60
        self.recent_prices = []  # Armazena últimos 5 preços

    async def monitor_and_trade(self):
        while True:
            if not self.telegram.running:
                print("QCT parado. Aguardando comando /start no Telegram.")
                logging.info("QCT parado.")
                await asyncio.sleep(1)
                continue

            current_time = time.time()
            if current_time - self.last_check_time >= self.check_interval:
                try:
                    ticker = self.client.get_ticker(self.symbol)
                    price = ticker['last_price']
                    volume = ticker.get('volume', 0)  # Volume do ticker
                    balance = self.client.get_balance()['total']
                    usdt_balance = balance.get('USDT', 0)
                    btc_balance = balance.get('BTC', 0)

                    # Atualiza histórico de preços (últimos 5)
                    self.recent_prices.append(price)
                    if len(self.recent_prices) > 5:
                        self.recent_prices.pop(0)

                    message = f"Monitorando {self.symbol}: Preço atual = {price} USDT, Volume = {volume}"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)

                    signal = self.grok.get_trading_signal(self.symbol, ticker, volume, self.recent_prices)
                    message = f"Sinal da Grok: {signal}"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)

                    if signal == 'buy' and usdt_balance > 10:
                        amount = 0.001
                        order = self.client.exchange.create_market_buy_order(self.symbol, amount)
                        self.last_buy_price = price
                        message = f"Compra executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)

                    elif signal == 'sell' and btc_balance >= 0.001:
                        amount = 0.001
                        order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                        message = f"Venda executada: {amount} BTC a {price} USDT (Sinal: {signal})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)
                        self.last_buy_price = None

                    elif self.last_buy_price and price < self.stop_loss and btc_balance >= 0.001:
                        amount = 0.001
                        order = self.client.exchange.create_market_sell_order(self.symbol, amount)
                        message = f"Stop-Loss acionado: Vendido {amount} BTC a {price} USDT (Compra em {self.last_buy_price})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)
                        self.last_buy_price = None

                    self.last_check_time = current_time

                except Exception as e:
                    error_message = f"Erro no monitoramento: {str(e)}"
                    print(error_message)
                    logging.error(error_message)
                    await self.telegram.send_message(error_message)

            await asyncio.sleep(1)