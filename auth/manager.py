from fastapi import HTTPException
from sqlalchemy import select, insert
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.schemas import RegisterUser, RefreshToken
from auth.services import TokenService
from core.manager import BaseManager


class AuthManager(BaseManager):
    def __init__(
            self,
            db:AsyncSession,

    ):
        super().__init__(db)
        self.token_service = TokenService()
    async def check_username(
            self,
            username: str,
    ):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        result = result.scalar_one_or_none()
        # if not result:
        #     return None
        # return False
        return True if not result else False

    async def register(
            self,
            request: RegisterUser
    ):
        # Проверяем юзернейм
        if not await self.check_username(request.username):
            raise HTTPException(
                status_code=409,
                detail="Username already exists.",
            )
        data = request.model_dump()  # fullname username email
        data.pop("password2")
        password = argon2.hash(data.pop("password1"))
        stmt = insert(User).values(
            **data,
            password=password
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def login(
            self,
            username: str,
            password: str,
    ):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password" #dict or str
            )
        if not argon2.verify(password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"  # dict or str
            )
        token = self.token_service.generate(user)
        return token


    async def refresh(self,request: RefreshToken):
        payload = self.token_service.validate(request.refresh_token, True)

        stmt = select(User).where(
            User.id==int(payload["sub"])
        )

        user = await self.db.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
            )
        token = self.token_service.generate(user)
        return token

    async def get_me(
            self,
            token: str
    ):
        payload = self.token_service.validate(token, False)

        stmt = select(User).where(
            User.id ==int(payload["sub"])
        )

        user = await self.db.execute(stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
        return user