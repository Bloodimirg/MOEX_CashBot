from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.handlers.states import BondStates
from bot.keyboards.menu import Keyboard
from bot.moex_API.parser import MoexAPI


class CallbackHandlers(MoexAPI):
    """Класс обработки вызовов"""
    def __init__(self, dp, bot, bond_handlers):
        super().__init__()
        self.dp = dp
        self.bot = bot
        self.keyboard = Keyboard()
        self.bond_handlers = bond_handlers
        self.setup_handlers()

    def setup_handlers(self):
        """Регистрация команд"""
        self.dp.callback_query.register(self.handle_callback)

    async def handle_callback(self, query: CallbackQuery, state: FSMContext):
        """Обработка обратных вызовов"""
        if query.data == "menu_bonds":
            await query.message.edit_text("Меню облигаций:", reply_markup=self.keyboard.bonds_menu())
        elif query.data == "menu_stocks":
            await query.message.edit_text("Меню акций", reply_markup=self.keyboard.stocks_menu())
        elif query.data == "back_to_main":
            await query.message.edit_text("Главное меню", reply_markup=self.keyboard.main_menu())
        elif query.data == "add_bond":
            await query.answer()
            await query.message.edit_text("Введите ISIN облигации...", reply_markup=query.message.reply_markup)
            await state.set_state(BondStates.waiting_for_bond_ticker)
        elif query.data == "show_bonds":
            await self.bond_handlers.show_bonds(query)

        else:
            await query.answer("")
