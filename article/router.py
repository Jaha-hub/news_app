from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import is_author, is_owner, get_article_or_404
from article.models import Article
from article.schemas import ArticleCreate, ArticleRead, ArticleUpdate, ArticleStatusUpdate
from article.services import create_article, update_article, delete_article
from auth.models import User
from core.dependencies import get_db

router = APIRouter(
    prefix="/article",
    tags=["article"]
)

@router.get(
    "/"
)
async def get_all(

):
    pass

@router.post(
    "/",
    status_code=201,
    response_model=ArticleRead,
    summary="Создание Статьи",
    responses={
        401: {
            "description":"Не авторизован"
        },
        403: {
            "description":"Нет прав"
        },
        404:{
            "description":"Категория не найдена"
        }
    }
)
async def create(
        request: ArticleCreate,
        user: User = Depends(is_author),
        session: AsyncSession = Depends(get_db)
):
    """
    Endpoint создания Статьи
    требует **авторизованного**, пользователя который имеет роль автора/админа
    """
    response = await create_article(session, request, user.id)
    return response

@router.put(
    "/{article_id}",
    dependencies=
    [
        Depends(is_owner)
     ],
    summary="Обновление статьи",
    responses={
        401: {
            "description": "Не авторизован"
        },
        403:{
            "description":"Нет прав"
        },
        404: {
            "description": "Статья не найдена"
        }
    }
)
async def update(
        request: ArticleUpdate ,
        session: AsyncSession = Depends(get_db),
        article: Article = Depends(get_article_or_404),
):
    """
    Изменение Статья

    :param request: Обновление Статьи
    :param session: Сессия БД
    :param article: Получение Статьи
    :return: Ничего
    """

    await update_article(session=session, article=article, request=request)

@router.get(
    "/{article_id}",
    status_code=200,
    summary="Получение статьи",
    responses={
        401: {
            "description":"Не авторизован"
        },
        404:{
            "description":"Статья не найдена"
        }
    }
)
async def get(
        article: Article = Depends(get_article_or_404),
):
    """

    :param article: получение статьи
    :return: статью
    """
    return article

@router.delete(
    "/{article_id}",
    status_code=204,
    summary="Удаление статьи",
    responses={
        401: {
            "description":"Не авторизован"
        },
        403: {
            "description":"Нет прав"
        },
        404:{
            "description":"Статья не найдена"
        }
    }
)
async def delete(
    session: AsyncSession = Depends(get_db),
    article: Article = Depends(get_article_or_404),
) -> None:
    """
    Удаление статьи
    :param session: Сессия БД
    :param article: получение статьи
    :return: ничего
    """
    await delete_article(session, article=article)

@router.patch(
    "/{article_id}",
    status_code=200,
    summary="Частичное обновление статьи",
    responses={
        401: {
            "description":"Не авторизован"
        },
        403: {
            "description":"Нет прав"
        },
        404:{
            "description":"Статья не найдена"
        }
    }
)
async def patch(
    request: ArticleStatusUpdate,
    session: AsyncSession = Depends(get_db),
    article: Article = Depends(get_article_or_404),
):
    """
    Частичное обновление статьи
    :param request: Обновление статуса статьи
    :param session: Сессия БД
    :param article: Получение статьи
    :return: ничего
    """
    await update_article(session=session, article=article, request=request)