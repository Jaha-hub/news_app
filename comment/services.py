from typing import List

from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from comment.models import Comment
from comment.schemas import CommentCreate


async def create_comment(
        session: AsyncSession,
        comment: CommentCreate,
        user_id: int,
        article_id: int,
)->Comment:
    """
    Создаём комментарий
    :param session: Сессия БД
    :param comment: Функция из схемы нас отсылает к CommentBase, от которого всё и зависит
    :param user_id: ID юзера из БД
    :param article_id: ID блога
    :return: комментарий
    """
    await get_article_or_404(article_id, session)
    comment = Comment(**comment.model_dump(), user_id=user_id,article_id=article_id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

async def get_comments(
        session: AsyncSession,
        article_id: int,
)->List[Comment]:
    """
    получение нескольких комментариев
    :param session: Сессия БД
    :param article_id: ID блога
    :return: комментарии из блога
    """
    stmt = Select(Comment).where(Comment.article_id == article_id)
    result = await session.execute(stmt)
    comments = result.scalars().all()
    return comments


async def get_comment(
        session: AsyncSession,
        comment_id: int,
)->Comment:
    """
    получение комментария по ID
    :param session:
    :param comment_id:
    :return: комментарий
    """
    stmt = Select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


async def delete_comment(
        session: AsyncSession,
        comment: Comment,
        user_id: int,
)->None:
    if user_id != comment.user_id:
        raise HTTPException(status_code=403, detail="Не достаточно прав")
    await session.delete(comment)
    await session.commit()