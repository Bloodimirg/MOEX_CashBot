from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.orm.bonds import add_bond, get_bonds, remove_bonds
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
        self.dp.message.register(self.process_bond_ticker, BondStates.waiting_add_bond_ticker)
        self.dp.message.register(self.process_bond_removal, BondStates.waiting_remove_bond_ticker)

    @staticmethod
    async def add_bond_start(message: Message, state: FSMContext):
        """Начало процесса добавления облигации."""
        await state.set_state(BondStates.waiting_add_bond_ticker)

    async def process_bond_ticker(self, message: types.Message, state: FSMContext):
        """Обработка тикера облигации для добавления."""
        try:
            ticker = message.text.strip()
            bond_data, error = self.check_bond_ticker(ticker)
            if bond_data is None:
                # облигация не существует или отсутствие по ней данных
                await message.answer(f"{ticker}\n{error}", reply_markup=self.keyboard.bonds_menu())
            else:
                result = add_bond(user_id=message.from_user.id, bond_data=bond_data[0])
                if result == 1:
                    await message.answer("Невозможно добавить новую облигацию.\nУ вас уже есть 10 облигаций.",
                                         reply_markup=self.keyboard.bonds_menu())
                elif result == 2:
                    await message.answer(f"{bond_data[0]['SHORTNAME']} уже добавлена.\n",
                                         reply_markup=self.keyboard.bonds_menu())
                elif result == 3:
                    await message.answer(f"{bond_data[0]['SHORTNAME']} добавлена.\n",
                                         reply_markup=self.keyboard.bonds_menu())

        finally:
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
            f"Название: {bond.shortname}, "
            f"\nISIN: {bond.secid}"
            f"\nКупон: {bond.couponvalue if bond.couponvalue is not None else 'Нет данных'} руб."
            f"\nСледующая выплата: {bond.nextcoupon if bond.nextcoupon is not None else 'Нет данных'}"
            f"\nПоследняя цена: {f'{bond.last}%' if bond.last is not None else 'Нет данных'}"
            f"\nРейтинг: {bond.status if bond.status is not None else 'Нет данных'}"
            f"\nДата погашения: {bond.matdate if bond.matdate is not None else 'Нет данных'}"
            f"\nИзменение цены за день: "
            f"{f'{bond.lasttoprevprice}%' if bond.lasttoprevprice is not None else 'Нет данных'}"
            f"\n------------"
            for bond in bonds]

        await query.message.edit_text("\n".join(bond_messages), reply_markup=self.keyboard.bonds_menu())

    async def remove_bond_start(self, query: types.CallbackQuery, state: FSMContext):
        """Начало процесса удаления облигации."""
        user_id = query.from_user.id
        bonds = get_bonds(user_id)

        if bonds:
            await query.message.edit_text("Выберите облигацию для удаления:",
                                          reply_markup=self.keyboard.bond_remove_buttons(bonds))
        else:
            await query.message.edit_text("У вас нет облигаций для удаления.", reply_markup=self.keyboard.bonds_menu())

        await state.set_state(BondStates.waiting_remove_bond_ticker)
        await state.clear()

    async def process_bond_removal(self, query: types.CallbackQuery, state: FSMContext):
        """Обработка тикера облигации для удаления."""
        bond_secid = query.data.split(":")[1]
        user_id = query.from_user.id

        try:
            result = remove_bonds(user_id, bond_secid)
            if result == 1:
                await query.answer(f"Облигация с ISIN {bond_secid} удалена.")
                updated_bonds = get_bonds(user_id)

                if updated_bonds:
                    await query.message.edit_text("Доступные облигации:\n\nВыберите облигацию для удаления:",
                                                  reply_markup=self.keyboard.bond_remove_buttons(updated_bonds))
                else:
                    await query.message.edit_text("У вас больше нет облигаций для удаления.",
                                                  reply_markup=self.keyboard.bonds_menu())

        except ValueError as e:
            await query.answer(str(e))
        finally:
            await state.clear()
