from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
from datetime import datetime

class WalletQuery(Base):
    __tablename__ = "wallet_queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
