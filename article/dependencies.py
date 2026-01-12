# Проверка то что пользователь автор
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.models import Article
from article.services import get_article
from auth.dependencies import get_current_user
from auth.models import User
from auth.schemas import RoleEnum
from core.dependencies import get_db


async def get_article_or_404(
        article_id: int,
        session:AsyncSession= Depends(get_db),
) -> Article:
    """
    Функция для проверки наличия статьи по ID

    :param article_id: ID статьи
    :param session: Зависимость Сессии БД

    :raise HTTPException: Статья не найдена

    :return: моделька Статьи
    """


    # Зависим от БД
    return await get_article(session=session, article_id=article_id)

async def is_author(
        user: User = Depends(get_current_user),
        # article: Article = Depends(get_article_or_404),
) -> User:
    """
    Функция для проверки роли автора пользователя

    :param user: зависимость авторизованного текущего пользователя

    :raise HTTPException: не имеет право создавать/обновлять статью
    :raise HTTPException: пользователь не авторизован
    :return: моделька пользователя
    """
    # Зависим от того то пользователь авторизован или нет
    if user.role not in [RoleEnum.author, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Вы не имеете право создавать/обновлять статью")
    return user
# Проверка на то что пользователь автор статьи
async def is_owner(
        user: User = Depends(is_author),
        article: Article = Depends(get_article_or_404)
) -> None:
    """
    функция для проверки статьи
    :param user: зависимость пользователя с ролью автор/админ
    :param article: зависимость от статьи

    :raise HTTPException: Недостаточно прав
    :raise HTTPException: Статья не найдена

    :return: Ничего
    """
    # Зависим от существования статьи
    # Зависим от того то пользователь авторизован или нет
    if article.author_id != user.id or user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав"
        )


