from sqlalchemy import Column, String, Boolean
from core.models import Base, IntIDMixin, TimeActionMixin


class User(Base, IntIDMixin, TimeActionMixin):
    __tablename__ = 'users'

    username = Column(String(320), unique=True, nullable=False)
    full_name = Column(String(320), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String(20), nullable=False, default='client')
    is_active = Column(Boolean, nullable=False, default=True)
    avatar = Column(String, nullable=True)
