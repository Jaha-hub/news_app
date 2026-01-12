import re
from pydantic import Field, EmailStr, field_validator, model_validator, BaseModel
from enum import Enum

class RefreshToken(BaseModel):
    refresh_token: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RoleEnum(str, Enum):
    client = "client",
    admin = "admin",
    moderator = "moderator",
    author = "author",




class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=320)
    full_name: str = Field(min_length=3, max_length=512)
    email: EmailStr

    @field_validator("username",mode="before")
    @classmethod
    def lower_username(cls, value):
        return value.lower()


class RegisterUser(UserBase):
    password1: str
    password2: str

    @field_validator("password1", "password2",mode="before")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен состоять минимум из 8 символов")
        if not re.search(r"[A-ZА-Я]", value):
            raise ValueError("Пароль должен состоять из минимум из одной заглавной буквы")
        if not re.search(r"[a-zа-я]",value):
            raise ValueError("Пароль должен состоять из минимум из одной строчной буквы")
        if not re.search(r"[0-9]",value):
            raise ValueError("Пароль должен состоять из минимум из одной цифры буквы")
        if not re.search(r"[\W_]",value):
            raise ValueError("Пароль должен состоять из минимум из одного спец символа")
        return value

    @model_validator(mode="after")
    def validate_check_password_match(self):
        if self.password1 != self.password2:
            raise ValueError("Пароли не совпадают")
        return self