
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.mysql import BIGINT

from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="INR")
    status = Column(String(20), nullable=False, default="pending")
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


def create_transaction_table():
    Base.metadata.create_all(
        bind=engine,
        tables=[Transaction.__table__],
    )