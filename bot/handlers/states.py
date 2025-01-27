from aiogram.fsm.state import State, StatesGroup


class BondStates(StatesGroup):
    """Состояние ожидания получения тикера облигации."""
    waiting_for_bond_ticker = State()
