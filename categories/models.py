from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime

from core.models import Base, IntIDMixin, TimeActionMixin


class Category(Base, IntIDMixin, TimeActionMixin):
    __tablename__ = 'categories'

    title = Column(String(256), nullable=False, unique=True)
    # slug = Column(String(256), nullable=False, unique=True)
    description = Column(String(1024), nullable=True)
    # created_at = Column(DateTime, nullable=False, default=datetime.now)