from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from article.models import Article
from auth.dependencies import get_current_user
from auth.models import User
from complaint.dependencies import get_complaint_or_404
from complaint.models import Complaint
from complaint.schemas import ComplaintCreate
from complaint.services import create_complaint, delete_complaint
from core.dependencies import get_db

router = APIRouter(
    prefix="/{article_id}/complaint",
    # prefix
    tags=["complaint"]
)

@router.get(
    "/{complaint_id}",
)
async def get_complaint(
        complaint: Complaint= Depends(get_complaint_or_404),
):
    """
    получение комментария
    """
    return complaint

@router.post(
    "/{complaint_id}",
)
async def create(
        complaint: ComplaintCreate,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        article: Article = Depends(get_article_or_404)
):
    response = await create_complaint(session, complaint, user_id=user.id, article_id=article.id)
    return response

@router.delete(
    "/{complaint_id}",
)
async def delete(
        session: AsyncSession = Depends(get_db),
        complaint: Complaint = Depends(get_complaint_or_404),
):
    await delete_complaint(session, complaint, user_id=complaint.user_id)
