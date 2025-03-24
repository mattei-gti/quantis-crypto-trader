from trading_logic import TradingLogic
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

trader = TradingLogic(API_KEY, SECRET_KEY)

# Executa o monitoramento em loop
asyncio.run(trader.monitor_and_trade())