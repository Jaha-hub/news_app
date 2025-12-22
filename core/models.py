from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class IntIDMixin:
    id = Column(BigInteger, primary_key=True, autoincrement=True)

class TimeActionMixin:
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)