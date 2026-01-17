from fastapi import FastAPI

from auth.router import router as auth_router
from categories.router import router as cat_router
from article.router import router as article_router
from comment.router import router as comment_router
from complaint.router import router as complaint_router
from bookmark.router import router as bookmark_router
from media.router import router as media_router
app = FastAPI(
    title="Jahangir"
)

article_router.include_router(comment_router)
article_router.include_router(complaint_router)
article_router.include_router(bookmark_router)
article_router.include_router(media_router)
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(cat_router)
