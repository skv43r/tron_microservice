"""
Модуль для настройки Tron клиента.
"""

from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.core.config import settings

tron = Tron(provider=HTTPProvider(settings.ENDPOINT_URI,
            api_key=settings.API_KEY))
