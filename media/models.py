from sqlalchemy import Column, BigInteger, ForeignKey, String

from core.models import Base, IntIDMixin


class ArticleImage(Base, IntIDMixin):
    __tablename__ = "articleimage"
    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"))
    filename = Column(String)
    file_path = Column(String)