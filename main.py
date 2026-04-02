import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
#from dotenv import load_dotenv

# Bizning modullar
from bot.commands import user_router
from bot.admin import admin_router
from database import init_db

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

class BotApp:
    def __init__(self):
        #load_dotenv()
        self.token = os.getenv("BOT_TOKEN")

        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        self.dp = Dispatcher()

        # Routerlarni ulaymiz
        self.dp.include_router(user_router)
        self.dp.include_router(admin_router)

    async def start(self):
        init_db()
        await self.dp.start_polling(self.bot)

if __name__ == "__main__":
    asyncio.run(BotApp().start())
