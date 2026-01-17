from sqlalchemy import Column, ForeignKey, Integer, String

from core.models import Base, IntIDMixin, TimeActionMixin


class Complaint(Base, IntIDMixin, TimeActionMixin):
    __tablename__ = 'complaints'

    body = Column(String(1024),nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id', ondelete="CASCADE"), nullable=False)
