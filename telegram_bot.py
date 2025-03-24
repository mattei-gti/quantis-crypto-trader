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

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    def start(self, update, context):
        self.running = True
        update.message.reply_text("QCT iniciado!")

    def stop(self, update, context):
        self.running = False
        update.message.reply_text("QCT parado!")

    def status(self, update, context):
        status = "QCT rodando" if self.running else "QCT parado"
        update.message.reply_text(status)

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("stop", self.stop))
        self.application.add_handler(CommandHandler("status", self.status))

    async def run(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)