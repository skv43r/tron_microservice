"""
Модуль конфигурации.
"""
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для хранения настроек.
    """
    MODE: Literal["DEV", "TEST"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_URL: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    TEST_DB_URL: str

    ENDPOINT_URI: str
    API_KEY: str

    class Config:
        """
        Конфигурация для класса Settings.
        """
        env_file = ".env"


settings = Settings()
