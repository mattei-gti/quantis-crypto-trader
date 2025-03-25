from telegram import Bot
from telegram.ext import Application, CommandHandler
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.token)
        self.application = Application.builder().token(self.token).build()
        self.running = False
        self.setup_handlers()
        self.trading_logic = None  # Referência ao TradingLogic será setada depois

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def start(self, update, context):
        self.running = True
        await update.message.reply_text("QCT iniciado!")

    async def stop(self, update, context):
        self.running = False
        await update.message.reply_text("QCT parado!")

    async def status(self, update, context):
        status = "QCT rodando" if self.running else "QCT parado"
        await update.message.reply_text(status)

    async def report(self, update, context):
        if self.trading_logic:
            await self.trading_logic.send_report()
        else:
            await update.message.reply_text("Erro: TradingLogic não configurado.")

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("status", self.status))
        self.application.add_handler(CommandHandler("report", self.report))

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)