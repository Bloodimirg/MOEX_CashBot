from aiogram.fsm.state import State, StatesGroup


class BondStates(StatesGroup):
    """Состояние ожидания получения тикера облигации."""
    waiting_add_bond_ticker = State()
    waiting_remove_bond_ticker = State()
