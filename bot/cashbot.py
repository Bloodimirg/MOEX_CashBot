import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from bot.database.orm.users import add_user
from bot.handlers.callback_handlers import CallbackHandlers
from bot.handlers.bond_handlers import BondHandlers
from bot.config import Base, engine
from bot.keyboards.menu import Keyboard

logging.basicConfig(level=logging.INFO)
load_dotenv()


class CashBot:
    """Основной бот"""
    def __init__(self):
        self.bot = Bot(os.getenv('API_TOKEN'))
        self.dp = Dispatcher()
        self.keyboard = Keyboard()
        self.bond_handlers = BondHandlers(self.dp, self.bot)
        self.callback_handlers = CallbackHandlers(self.dp, self.bot, self.bond_handlers)
        self.setup_handlers()

    def setup_handlers(self):
        """Регистрация глобальных обработчиков"""
        self.dp.message.register(self.start_command, Command("start"))
        BondHandlers(self.dp, self.bot)

    async def start_command(self, message: Message):
        """Обрабочик команды /start"""
        telegram_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        add_user(telegram_id, username, full_name)
        await message.answer("Добро пожаловать!", reply_markup=self.keyboard.main_menu())

    async def on_start(self):

        Base.metadata.create_all(bind=engine)
        await self.dp.start_polling(self.bot)
