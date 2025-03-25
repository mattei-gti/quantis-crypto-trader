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
        self.telegram.trading_logic = self  # Conecta ao TelegramBot
        self.grok = GrokClient()
        self.symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
        self.stop_loss = {'BTC/USDT': 84000, 'ETH/USDT': 2500, 'BNB/USDT': 500}
        self.last_buy_price = {symbol: None for symbol in self.symbols}
        self.last_check_time = 0
        self.check_interval = 60
        self.recent_prices = {symbol: [] for symbol in self.symbols}
        self.min_notional = {'BTC/USDT': 10, 'ETH/USDT': 10, 'BNB/USDT': 10}
        self.trades = {symbol: {'buy': 0, 'sell': 0, 'total_usdt': 0} for symbol in self.symbols}

    async def send_report(self):
        balance = self.client.get_balance()['total']
        report = "Relatório do QCT:\n"
        total_usdt = balance.get('USDT', 0)
        
        for symbol in self.symbols:
            base_currency = symbol.split('/')[0]
            base_balance = balance.get(base_currency, 0)
            last_price = self.recent_prices[symbol][-1] if self.recent_prices[symbol] else 0
            value_usdt = base_balance * last_price
            total_usdt += value_usdt
            trades = self.trades[symbol]
            report += (f"{symbol}: Saldo = {base_balance:.4f} {base_currency}, "
                      f"Valor = {value_usdt:.2f} USDT, "
                      f"Compras = {trades['buy']}, Vendas = {trades['sell']}, "
                      f"Total USDT negociado = {trades['total_usdt']:.2f}\n")
        
        report += f"Saldo Total Estimado: {total_usdt:.2f} USDT"
        print(report)
        logging.info(report)
        await self.telegram.send_message(report)

    async def monitor_and_trade(self):
        while True:
            if not self.telegram.running:
                print("QCT parado. Aguardando comando /start no Telegram.")
                logging.info("QCT parado.")
                await asyncio.sleep(1)
                continue

            current_time = time.time()
            if current_time - self.last_check_time < self.check_interval:
                await asyncio.sleep(1)
                continue

            try:
                balance = self.client.get_balance()['total']
                usdt_balance = balance.get('USDT', 0)

                for symbol in self.symbols:
                    ticker = self.client.get_ticker(symbol)
                    price = ticker['last_price']
                    volume = ticker.get('volume', 0)
                    base_currency = symbol.split('/')[0]
                    base_balance = balance.get(base_currency, 0)

                    self.recent_prices[symbol].append(price)
                    if len(self.recent_prices[symbol]) > 5:
                        self.recent_prices[symbol].pop(0)

                    message = f"Monitorando {symbol}: Preço atual = {price} USDT, Volume = {volume}"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)

                    signal = self.grok.get_trading_signal(symbol, ticker, volume, self.recent_prices[symbol])
                    message = f"Sinal da Grok para {symbol}: {signal}"
                    print(message)
                    logging.info(message)
                    await self.telegram.send_message(message)

                    amount = max(0.001, self.min_notional[symbol] / price)

                    if signal == 'buy' and usdt_balance > self.min_notional[symbol]:
                        order = self.client.exchange.create_market_buy_order(symbol, amount)
                        self.last_buy_price[symbol] = price
                        self.trades[symbol]['buy'] += 1
                        self.trades[symbol]['total_usdt'] += amount * price
                        message = f"Compra executada: {amount} {base_currency} a {price} USDT (Sinal: {signal})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)

                    elif signal == 'sell' and base_balance >= amount:
                        order = self.client.exchange.create_market_sell_order(symbol, amount)
                        self.trades[symbol]['sell'] += 1
                        self.trades[symbol]['total_usdt'] += amount * price
                        message = f"Venda executada: {amount} {base_currency} a {price} USDT (Sinal: {signal})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)
                        self.last_buy_price[symbol] = None

                    elif (self.last_buy_price[symbol] and 
                          price < self.stop_loss[symbol] and 
                          base_balance >= amount):
                        order = self.client.exchange.create_market_sell_order(symbol, amount)
                        self.trades[symbol]['sell'] += 1
                        self.trades[symbol]['total_usdt'] += amount * price
                        message = f"Stop-Loss acionado: Vendido {amount} {base_currency} a {price} USDT (Compra em {self.last_buy_price[symbol]})"
                        print(message)
                        logging.info(message)
                        await self.telegram.send_message(message)
                        self.last_buy_price[symbol] = None

                self.last_check_time = current_time

            except Exception as e:
                error_message = f"Erro no monitoramento: {str(e)}"
                print(error_message)
                logging.error(error_message)
                await self.telegram.send_message(error_message)

            await asyncio.sleep(1)