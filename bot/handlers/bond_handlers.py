from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.orm.bonds import add_bond, get_bonds
from bot.handlers.states import BondStates
from bot.keyboards.menu import Keyboard
from bot.moex_API.parser import MoexAPI


class BondHandlers(MoexAPI):
    """Класс обработки команд, связанных с облигациями."""
    def __init__(self, dp, bot):
        super().__init__()
        self.dp = dp
        self.bot = bot
        self.keyboard = Keyboard()
        self.register_handlers()

    def register_handlers(self):
        """Регистрация локальных обработчиков"""
        self.dp.message.register(self.add_bond_start, Command("add_bond"))
        self.dp.message.register(self.show_bonds, Command("show_bonds"))
        self.dp.message.register(self.process_bond_ticker, BondStates.waiting_for_bond_ticker)

    @staticmethod
    async def add_bond_start(message: Message, state: FSMContext):
        """Начало процесса добавления облигации."""
        await message.edit_text("Введите тикер облигации (например, RU000A106UW3):")
        await state.set_state(BondStates.waiting_for_bond_ticker)

    async def process_bond_ticker(self, message: types.Message, state: FSMContext):
        """Обработка тикера облигации для добавления."""
        ticker = message.text.strip()
        bond_data, error = self.check_bond_ticker(ticker)
        bond_info = bond_data[0]

        if error:
            await message.answer(f"{ticker}\n{error}", reply_markup=self.keyboard.bonds_menu())
        else:
            if not add_bond(user_id=message.from_user.id, bond_data=bond_info):
                await message.answer(f"{bond_info['SHORTNAME']} уже добавлена.\n",
                                     reply_markup=self.keyboard.bonds_menu())
            else:
                await message.answer(f"{bond_info['SHORTNAME']} добавлена.\n", reply_markup=self.keyboard.bonds_menu())

        await state.clear()

    async def show_bonds(self, query: types.CallbackQuery):
        """Обработчик нажатия кнопки для отображения облигаций."""
        user_id = query.from_user.id
        bonds = get_bonds(user_id)

        await query.answer()

        if not bonds:
            await query.message.edit_text("У вас нет облигаций.", reply_markup=self.keyboard.main_menu())
            return

        bond_messages = [
            f"Тикер: {bond.secid}, \nНазвание: {bond.shortname}, \nЦена: {bond.prevwaprice}"
            f"\nДоходность: {bond.yieldatprevwaprice}"
            for bond in bonds]

        await query.message.edit_text("\n".join(bond_messages), reply_markup=self.keyboard.main_menu())
