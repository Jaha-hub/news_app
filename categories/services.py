from fastapi import HTTPException
from sqlalchemy import select

from categories.filters import CategoryFilter
from categories.models import Category

from sqlalchemy.ext.asyncio import AsyncSession
from categories.schemas import CategoryCreate, CategoryUpdate, CategoryRead


async def create_category(db: AsyncSession, request: CategoryCreate) -> Category:
    category = Category(
        **request.model_dump()
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

async def update_category(db: AsyncSession, category: Category, request:CategoryUpdate) -> None:
    category.name = request.name
    category.description = request.description

    db.add(category)
    await db.commit()

async def get_category(
    db: AsyncSession,
    category_id: int,
):
    stmt = select(Category).where(Category.id == category_id)
    result = await db.execute(stmt)
    category = result.scalars().one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category not found{category_id}")
    return category

async def delete_category(db: AsyncSession, category:Category) -> None:
    await db.delete(category)
    await db.commit()


async def get_categories(
    db: AsyncSession,
    filters: CategoryFilter,

) -> list[Category]:
    stmt = select(Category)
    stmt = filters.filter(stmt)
    stmt = filters.sort(stmt)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return categories