from sqlalchemy import Column, ForeignKey, BigInteger, UniqueConstraint

from core.models import Base, IntIDMixin, TimeActionMixin


class Bookmark(Base, IntIDMixin,TimeActionMixin):
    __tablename__ = "bookmarks"

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(BigInteger, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)



    __table_args__ = (
        UniqueConstraint("user_id", "article_id"),
    )