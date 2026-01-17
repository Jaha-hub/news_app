from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger

from core.models import Base, IntIDMixin, TimeActionMixin


class Comment(Base,IntIDMixin, TimeActionMixin):
    __tablename__ = 'comments'

    body = Column(String(2048), nullable=False)
    article_id = Column(BigInteger, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)