from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from article.dependencies import get_article_or_404
from complaint.services import get_complaint
from core.dependencies import get_db
from article.models import Article

async def get_complaint_or_404(
        complaint_id: int,
        article: Article = Depends(get_article_or_404),
        session: AsyncSession = Depends(get_db),
):
    complaint = await get_complaint(session,complaint_id)
    if complaint.article_id != article.id:
        raise HTTPException(status_code=404, detail="Not found")
    return complaint