from fastapi import HTTPException
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from complaint.models import Complaint
from article.dependencies import get_article_or_404
from complaint.schemas import ComplaintCreate


async def create_complaint(
        session: AsyncSession,
        complaint: ComplaintCreate,
        user_id: int,
        article_id: int,
)->Complaint:
    await get_article_or_404(article_id, session)
    complaint = Complaint(**complaint.model_dump(),user_id =user_id, article_id=article_id)
    session.add(complaint)
    await session.commit()
    await session.refresh(complaint)
    return complaint

async def get_complaint(
        session: AsyncSession,
        complaint_id: int,
):
    stmt = Select(Complaint).where(Complaint.id == complaint_id)
    result = await session.execute(stmt)
    complaint = result.scalar_one_or_none()
    if not complaint:
        raise HTTPException(status_code=404, detail="No complaint found")
    return complaint



async def delete_complaint(
        session: AsyncSession,
        complaint: Complaint,
        user_id: int,
):
    if user_id != complaint.user_id:
        raise HTTPException(status_code=403, detail="Не достаточно прав")
    await session.delete(complaint)
    await session.commit()