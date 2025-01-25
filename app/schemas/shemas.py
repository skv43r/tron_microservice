from pydantic import BaseModel
from typing import List

class WalletResponse(BaseModel):
    bandwidth: int
    energy: int
    balance: float

class PaginatedResponse(BaseModel):
    total: int
    items: List[dict]

    class Config:
        arbitrary_types_allowed = True
        exclude = {"__sa_instance_state__"}
