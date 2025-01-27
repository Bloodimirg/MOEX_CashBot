from bot.config import SessionLocal
from bot.database.models.users import User


def add_user(telegram_id: int, username: str = None, full_name: str = None):
    """Добавление пользователя в БД"""
    session = SessionLocal()
    try:
        existing_user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if existing_user:
            print(f"Пользователь {username} уже существует.")
            return existing_user
        new_user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"Пользователь {username} успешно добавлен.")
        return new_user
    except Exception as e:
        print(f"Ошибка добавления: {e}")
    finally:
        session.close()
