from telegram import Bot
from telegram.ext import Updater
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.token)

    async def send_message(self, message):
        """Envia uma mensagem para o chat configurado."""
        await self.bot.send_message(chat_id=self.chat_id, text=message)