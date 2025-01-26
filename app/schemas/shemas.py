"""
Схемы данных для работы с API.
"""

from pydantic import BaseModel
from typing import List


class WalletResponse(BaseModel):
    """
    Схема ответа для информации о кошельке.
    """
    bandwidth: int
    energy: int
    balance: float


class PaginatedResponse(BaseModel):
    """
    Схема ответа для пагинированных данных.
    """
    total: int
    items: List[dict]

    class Config:
        arbitrary_types_allowed = True
        exclude = {"__sa_instance_state__"}
