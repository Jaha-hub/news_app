from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime

from core.models import Base, IntIDMixin, TimeActionMixin


class Article(Base, IntIDMixin, TimeActionMixin):
    __tablename__ = 'articles'

    title = Column(String(512), nullable=False)
    content = Column(Text,nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="SET NULL"))
    author_id = Column(Integer, ForeignKey('users.id', ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default='draft')
    published_at = Column(DateTime)
