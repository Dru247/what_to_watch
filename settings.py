"""Настройки проекта."""
import os


class Config(object):
    """Класс настроек."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
