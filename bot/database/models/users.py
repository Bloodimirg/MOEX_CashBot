from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from bot.config import Base
from datetime import datetime


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    date_joined = Column(DateTime, default=datetime.now)

    bonds = relationship("Bond", back_populates="user")  # Обратная связь с облигациями
