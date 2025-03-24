from trading_logic import TradingLogic
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

async def main():
    trader = TradingLogic(API_KEY, SECRET_KEY)
    
    # Inicia o Telegram Bot e o monitoramento como corrotinas
    telegram_task = asyncio.create_task(trader.telegram.run())
    trading_task = asyncio.create_task(trader.monitor_and_trade())
    
    # Aguarda ambas as tarefas
    await asyncio.gather(telegram_task, trading_task)

if __name__ == "__main__":
    asyncio.run(main())