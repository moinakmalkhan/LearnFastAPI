from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    id: Optional[int]
    content: str
    title: str
    is_published: Optional[bool]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserDetail(BaseModel):
    id: int
    email: EmailStr
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str
    token_type: str


class TokenWithUser(Token):
    user: UserDetail
