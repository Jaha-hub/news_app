from typing import List

from sqlalchemy import Delete, Select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from bookmark.models import Bookmark
from bookmark.schemas import BookmarkCreate


async def add_to_bookmark(
        session: AsyncSession,
        request: BookmarkCreate,
        user_id: int,
) -> None:
    """

    :param session: Сессия БД
    :param request: создание избранного
    :param user_id: ИД юзера
    :return: ничего
    """

    await get_article_or_404(request.article_id, session)
    bookmark = Bookmark(
        article_id=request.article_id,
        user_id=user_id,
    )
    session.add(bookmark)
    await session.commit()


async def remove_from_bookmark(
        session: AsyncSession,
        article_id: int,
        user_id: int,
) -> None:
    """

    :param session: Сессия БД
    :param article_id: ИД артикля
    :param user_id: ИД юзера
    :return: ничего
    """


    stmt = Delete(Bookmark).where(Bookmark.article_id == article_id, Bookmark.user_id == user_id)
    result = await session.execute(stmt)
    await session.commit()

async def get_user_bookmark(
        session: AsyncSession,
        user_id: int,
)-> List[Article]:
    """

    :param session: Сессия БД
    :param user_id: ИД юзера
    :return: пользователя
    """
    stmt = Select(Article).join(Bookmark).where(Bookmark.user_id == user_id)
    result = await session.execute(stmt)
    articles = result.scalars().all()
    return articles