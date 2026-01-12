from fastapi import FastAPI

from auth.router import router as auth_router
from categories.router import router as cat_router
from article.router import router as article_router

app = FastAPI(
    title="Jahangir"
)

app.include_router(auth_router)
app.include_router(cat_router)
app.include_router(article_router)