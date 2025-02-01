from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        """Главное меню"""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Облигации", callback_data="menu_bonds")],
                [InlineKeyboardButton(text="Акции", callback_data="menu_stocks")],
            ]
        )

    @staticmethod
    def bonds_menu():
        """Меню облигаций"""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Добавить облигацию", callback_data="add_bond")],
                [InlineKeyboardButton(text="Удалить облигацию", callback_data="remove_bond")],
                [InlineKeyboardButton(text="Просмотреть облигации", callback_data="show_bonds")],
                [InlineKeyboardButton(text="Назад", callback_data="back_to_main")],
            ]
        )

    @staticmethod
    def stocks_menu():
        """Меню акций"""
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Добавить акцию", callback_data="add_stock")],
                [InlineKeyboardButton(text="Удалить акцию", callback_data="remove_stock")],
                [InlineKeyboardButton(text="Просмотреть акции", callback_data="view_stocks")],
                [InlineKeyboardButton(text="Назад", callback_data="back_to_main")],
            ]
        )

    @staticmethod
    def bond_remove_buttons(bonds):
        """Создает кнопки для удаления облигаций."""
        bond_buttons = [
            [InlineKeyboardButton(text=f"{bond.shortname} (ISIN: {bond.secid})",
                                  callback_data=f"remove_bond:{bond.secid}")]
            for bond in bonds
        ]

        bond_buttons.append([InlineKeyboardButton(text="Назад", callback_data="menu_bonds")])

        return InlineKeyboardMarkup(inline_keyboard=bond_buttons)
