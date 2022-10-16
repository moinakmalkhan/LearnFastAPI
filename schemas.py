from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Post(BaseModel):
    id: int | None = Field(default=None, title="The ID of the post", gt=0)
    content: str = Field(title="The content of post", max_length=500)
    title: str = Field(title="The title of post", max_length=100)
    is_published: bool | None = Field(default=False, title="The status of post")
    created_at: datetime | None = Field(default=datetime.now(), title="The time when post was created")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "content": "This is a post",
                "title": "Post 1",
                "is_published": True
            }
        }


class User(BaseModel):
    email: EmailStr = Field(title="The email of user")
    password: str = Field(title="The password of user", max_length=100)

    class Config:
        orm_mode = True

class UserDetail(BaseModel):
    id: int = Field(title="The ID of user", gt=0)
    email: EmailStr = Field(title="The email of user")
    is_active: bool = Field(default=True, title="The status of user")
    created_at: datetime = Field(default=datetime.now(), title="The time when user was created")

    class Config:
        orm_mode = True


class Token(BaseModel):
    token: str = Field(title="The token of user")
    token_type: str = Field(default="Bearer", title="The type of token")


class TokenWithUser(Token):
    user: UserDetail = Field(title="The user detail")
