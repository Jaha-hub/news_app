from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from article.models import Article
from article.schemas import ArticleCreate, ArticleUpdate, ArticlesStatusEnum, ArticleStatusUpdate
from categories.dependencies import get_category_or_404

async def create_article(
        session: AsyncSession,
        request: ArticleCreate,
        author_id :int,
) -> Article:
    """
    Функция для создания модельки Article в БД

    :param session: Сессия БД
    :param request: Запрос с данными
    :param author_id: ID пользователя который создаёт статью

    :raise HTTPException: Не найдена категория

    :return: созданную статью
    """
    await get_category_or_404(request.category_id, session)
    article = Article(**request.model_dump(), author_id=author_id)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


async def update_article(
        session: AsyncSession,
        article: Article,
        request: ArticleUpdate | ArticleStatusUpdate,
) -> None:
    """
    обновляет запись модельки статьи

    если статус поменялся на публикованный то указывается время публикации
    Если категория статьи поменялась то проверяет наличие категории

    :param session: Сессия БД
    :param article: моделька статьи
    :param request: Запрос с обновлёнными данными Статьи

    :raise HTTPException: Не найдена Категория

    :return: ничего
    """

    if article.status != ArticlesStatusEnum.published and request.status == ArticlesStatusEnum.published:
        article.published_at = datetime.now()
    # setattr(article, "title", "Test")


    if article.category_id != request.category_id:
        raise get_category_or_404(request.category_id, session)
    for key, value in request.model_dump().items():
        setattr(article, key, value)
    session.add(article)
    await session.commit()


async def delete_article(
        session: AsyncSession,
        article: Article,
):
    """
    Удаляет запись модельку статьи из БД

    :param session:  Сессия БД
    :param article: моделька статьи
    :return: Ничего
    """

    await session.delete(article)
    await session.commit()


async def get_articles(

):
    pass

async def get_article(
        session: AsyncSession,
        article_id: int,
):
    """
    возвращает статьи из БД

    :param session: Сессия БД
    :param article_id: ID Статьи

    :raise HTTPException: Не найдена статья

    :return: статьи
    """

    stmt = Select(Article).where(
        Article.id == article_id
    )
    result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404)
    return article