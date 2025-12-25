from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from categories.models import Category
from core.manager import BaseManager

class CategoryManager(BaseManager):
    async def create_category(self, db:AsyncSession):
        stmt = insert(Category).values(
            title=Category.title,
            slug=Category.slug,
            description=Category.description,
            seo_title=Category.seo_title,
            seo_description=Category.seo_description,
        )
        result = await db.execute(stmt)
