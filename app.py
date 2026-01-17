from fastapi import FastAPI

from auth.router import router as auth_router
from categories.router import router as cat_router
from article.router import router as article_router
from comment.router import router as comment_router
app = FastAPI(
    title="Jahangir"
)
article_router.include_router(comment_router)

app.include_router(auth_router)
app.include_router(cat_router)
app.include_router(article_router)