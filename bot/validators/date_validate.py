from datetime import datetime


def validate_date(date_str):
    """Проверка корректности даты."""
    if date_str == "0000-00-00":
        return None
    try:
        if not date_str:
            return None
        return datetime.strptime(date_str, "%Y-%m-%d")

    except ValueError:
        return None


def fill_none(bond_data):
    """Заполняет поля со значением None строкой 'Нет данных'."""
    for key, value in bond_data.items():
        if value is None:
            bond_data[key] = "Нет данных"
    return bond_data
