import os
import shutil
from pathlib import Path

from fastapi import UploadFile, HTTPException
from passlib.ifc import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from article.models import Article
from article.schemas import ArticleRead
from media.models import ArticleImage

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES =(["image/jpeg", "image/png", "image/webp","image/jpg"])

async def save_upload_file(
        upload_file,
)-> str:
    dest = UPLOAD_DIR / f"{upload_file.filename}"

    with open("wb") as buffer:
        shutil.copyfileobj(upload_file, buffer)
    return f"{UPLOAD_DIR}/{upload_file.filename}"

async def upload(
        session: AsyncSession,
        article_id: int,
        upload_file: UploadFile,
):
    if upload_file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Неверный тип контента: {upload_file.content_type}",
        )
    file_path = await save_upload_file(upload_file)

    file_image = ArticleImage(
        article_id=article_id,
        filename=upload_file.filename,
        file_path=file_path,
    )
    session.add(file_image)
    await session.commit()
    return{
        "status": "success",
    }


async def download(
        session: AsyncSession,
        article: Article,
        file_id: int,
):
    stmt = select(ArticleImage).where(ArticleImage.article_id == file_id,ArticleImage.id == file_id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Изображение не найдено"
        )
    p = Path(image.file_path)
    if not p.exists():
        raise HTTPException(
            status_code=404,
            detail="Изображение не найдено"
        )
    return FileResponse(
        path=str(p),
        filename=image.filename,
    )

async def delete(
        session: AsyncSession,
        article: Article,
        file_id: int,
):
    stmt = select(ArticleImage).where(ArticleImage.article_id == file_id, ArticleImage.id == file_id)
    result = await session.execute(stmt)
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(
            status_code=404,
            detail="Изображение не найдено"
        )
    p = Path(image.file_path)
    if not p.exists():
        raise HTTPException(
            status_code=404,
            detail="Изображение не найдено"
        )
    await session.delete(image)
    try:
        os.remove(str(p))
    except OSError:
        pass
    await session.commit()