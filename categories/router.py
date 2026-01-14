from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter import FilterDepends

from categories.dependencies import get_category_or_404
from categories.filters import CategoryFilter
from categories.models import Category
from categories.schemas import CategoryCreate, CategoryRead, CategoryUpdate
from categories.services import get_category, create_category, update_category, delete_category

from core.dependencies import get_db
from core.session import async_session

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post(
    "/create_cat"
)
async def create(
        request: CategoryCreate,
        db: AsyncSession = Depends(get_db)
):
    response = await create_category(db, request)
    return response

@router.get(
    "/get_category_by_id",
)
async def get_category_by_id(
        category_id: int,
        request: CategoryRead,
        db: AsyncSession = Depends(get_db)
):
    response = await get_category(request, db, category_id)
    return response

@router.put(
    "/{category_id}"
)
async def update(
        request: CategoryUpdate,
        category: Category = Depends(get_category_or_404),
        db: AsyncSession = Depends(get_db)
):
    await update_category(db,category, request)

@router.delete(
    "/{category_id}"
)
async def delete(
        category: Category = Depends(get_category_or_404),
        db: AsyncSession = Depends(get_db)
):
    await delete_category(db,category)
@router.get(
    "/"
)
async def get_all(
        session: AsyncSession = Depends(async_session),
        filters: CategoryFilter = FilterDepends(CategoryFilter),
):
    response = await get_all(session, filters)
    return response