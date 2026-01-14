from fastapi import APIRouter, Depends
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from auth.dependencies import get_current_user
from auth.models import User
from comment.dependencies import get_comment_or_404
from comment.models import Comment
from comment.schemas import CommentCreate
from comment.services import get_comments, create_comment
from core.dependencies import get_db

router = APIRouter(
    prefix="/{article_id}/comment",
    # prefix
    tags=["comment"]
)

@router.get(
    "/{comment_id}",
)
async def get_comment(
        comment: Comment = Depends(get_comment_or_404),
):
    """
    получение комментария
    """
    return comment

@router.get(
    "/",
)
async def get_commentes(
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db),
):
    comments = await get_comments(session, article_id=article.id)
    return comments


@router.post(
    "/",
)
async def create(
        comment: CommentCreate,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        article: Article = Depends(get_article_or_404),
):
    """
    создание комментария
    """
    response = await create_comment(session,comment,user_id=user.id,article_id=article.id)
    return response


@router.delete(
    "/",
)
async def delete_comment(
        session: AsyncSession = Depends(get_db),
        comment: Comment = Depends(get_comment_or_404),
):
    """
    удаление комментариев комментария
    """
    await delete_comment(session, comment=comment)