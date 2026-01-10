from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from categories.services import get_category
from categories.models import Category
from core.dependencies import get_db


async def get_category_or_404(
    category_id: int = Path(ge=1),
    session: AsyncSession = Depends(get_db),
)-> Category:
    category = await get_category(session, category_id)
    return category