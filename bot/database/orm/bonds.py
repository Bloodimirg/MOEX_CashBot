from bot.config import SessionLocal
from bot.database.models import Bond


def add_bond(user_id: int, bond_data: dict):
    """Добавление облигации в БД"""
    session = SessionLocal()
    bond_data_lower = {key.lower(): value for key, value in bond_data.items()}
    # изменение названия зарезервированого ключа
    bond_data_lower["yield_value"] = bond_data_lower.pop("yield", None)

    bond_data_lower["user_id"] = user_id

    # фильтр на уже существующую облигацию в БД по secid
    existing_bond = session.query(Bond).filter_by(user_id=user_id, secid=bond_data_lower["secid"]).first()
    if existing_bond:
        print("Эта облигация уже добавлена.")
        session.close()
        return False

    bond = Bond(**bond_data_lower)
    session.add(bond)
    session.commit()
    session.close()
    print("Записано в БД")
    return True


def get_bonds(telegram_id: int):
    """Получение облигаций из БД"""
    session = SessionLocal()
    bonds = (
        session.query(Bond.secid, Bond.shortname, Bond.prevwaprice, Bond.yieldatprevwaprice)
        .filter(Bond.user_id == telegram_id)
        .all()
    )
    session.close()
    return bonds
