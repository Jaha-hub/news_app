from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category
from core.manager import BaseManager

class CategoryManager(BaseManager):
    async def create_с(self, db:AsyncSession):
        stmt = insert(Category).values(
            title=Category.title,
            description=Category.description,
        )
        result = await db.execute(stmt)
