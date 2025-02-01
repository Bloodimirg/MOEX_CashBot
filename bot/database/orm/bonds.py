from sqlalchemy.exc import SQLAlchemyError

from bot.config import SessionLocal
from bot.database.models import Bond
from bot.validators.date_validate import validate_date


def add_bond(user_id: int, bond_data: dict):
    """Добавление облигации в БД"""
    session = SessionLocal()

    try:
        bond_data_lower = {key.lower(): value for key, value in bond_data.items()}

        # изменение названия ключа, (yield зарезервировано)
        bond_data_lower["yield_value"] = bond_data_lower.pop("yield", None)

        bond_data_lower["user_id"] = user_id

        # счетчик количества бумаг пользователя
        user_bonds_count = session.query(Bond.id).filter_by(user_id=user_id).count()

        # фильтр уже добавленной бумаги
        existing_bond = session.query(Bond).filter_by(user_id=user_id, secid=bond_data_lower["secid"]).first()

        if user_bonds_count >= 10:
            return 1

        if existing_bond:
            return 2
        # заполнение полей Null
        # bond_data_lower = fill_none(bond_data_lower)

        # валидация дат
        bond_data_lower["nextcoupon"] = validate_date(bond_data_lower["nextcoupon"])
        bond_data_lower["matdate"] = validate_date(bond_data_lower["matdate"])
        bond_data_lower["prevdate"] = validate_date(bond_data_lower["prevdate"])
        bond_data_lower["offerdate"] = validate_date(bond_data_lower["offerdate"])

        bond = Bond(**bond_data_lower)
        session.add(bond)
        session.commit()
        return 3

    except ValueError as ve:
        print(f"Ошибка валидации: {ve}")
        return 4  # Код ошибки для валидации

    except SQLAlchemyError as e:
        print(f"Ошибка базы данных: {e}")
        session.rollback()
        return 5  # Код ошибки для базы данных

    finally:
        session.close()


def get_bonds(telegram_id: int):
    """Получение облигаций из БД"""
    session = SessionLocal()
    bonds = (
        session.query(Bond.secid,
                      Bond.shortname,
                      Bond.couponvalue,
                      Bond.nextcoupon,
                      Bond.last,
                      Bond.status,
                      Bond.matdate,
                      Bond.lasttoprevprice,
                      )
        .filter(Bond.user_id == telegram_id)
        .all()
    )
    session.close()
    return bonds


def remove_bonds(telegram_id: int, bond_ticker: str):
    """Удаление облигации по тикеру"""
    session = SessionLocal()

    try:

        bond = session.query(Bond).filter_by(user_id=telegram_id, secid=bond_ticker).first()

        if not bond:
            raise ValueError("Облигация не найдена для данного пользователя")

        session.delete(bond)
        session.commit()
        return 1

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
