from typing import Optional

from pydantic import BaseModel, validator, Field


class PostBase(BaseModel):
    post_title: str
    content: str = Field(..., min_length=10, max_length=30)

    @validator('post_title')
    def check_title(cls, v):
        if len(v) < 3:
            raise ValueError("Название должнол быть больше 3")
        return v


class PostList(PostBase):
    id: int
    post_slug: str
    published: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "post_title": "Post about nature",
                "post_slug": "nature",
                "content": "Something about nature",
                "published": True,
            }
        }


class AddPost(BaseModel):
    post_title: str
    post_slug: str
    content: str
    user_id: int


class UpdatePost(BaseModel):
    post_title: Optional[str] = ''
    post_slug: Optional[str] = ''
    published: Optional[bool] = False
    content: Optional[str] = ''


class ShowPost(BaseModel):
    id: int
    post_title: str
    post_slug: str
    content: str


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    name: str
    surname: str
    patronymic: str
    city: str
    age: int
    about_me: str

    @validator('age')
    def check_age_user(cls, value):
        if value <= 16:
            raise ValueError("Вам должно быть больше 16 лет")
        return value


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ShowUser(BaseModel):
    username: str
    email: Optional[str] = None
