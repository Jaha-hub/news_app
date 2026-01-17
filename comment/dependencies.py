from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from comment.models import Comment
from comment.services import get_comment
from core.dependencies import get_db



async def get_comment_or_404(
        comment_id: int,
        article: Article = Depends(get_article_or_404),
        session : AsyncSession = Depends(get_db)
)-> Comment:
    """
    функция зависимости комментария
    :param comment_id: ID комментария
    :param article: моделька статьи
    :param session: Сессия БД
    :raise HTTPException: Комментарий не найден

    :return: моделька комментария
    """
    comment = await get_comment(session=session,comment_id=comment_id)
    if comment.article_id != article.id:
        raise HTTPException(status_code=404,detail="Not Found")
    return comment