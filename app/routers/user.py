from datetime import timedelta, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select

from core.models.model import user, user_details, post
from core.schemas.schemes import RegisterUser, ShowPost, Token, ShowUser
from db import database
from app import dependencies

router = APIRouter(prefix="/user")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


async def authenticate_user(db_model, username: str, password: str):
    user_dict = await database.fetch_one(db_model.select().where(db_model.c.username == username))
    if not user_dict:
        return None
    if not verify_password(password, dict(user_dict.items())["password"]):
        return None
    return user_dict


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = await authenticate_user(db_model=user, username=form_data.username, password=form_data.password)
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=dependencies.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dependencies.create_access_token(
        data={"sub": dict(user_data.items())["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=ShowUser)
def read_users_me(current_user: ShowUser = Depends(dependencies.get_current_user)):
    return current_user


@router.post("/register")
async def register(data_user: RegisterUser):
    hash_password = get_password_hash(data_user.password)
    query_user = user.insert().values(
        username=data_user.username,
        email=data_user.email,
        password=hash_password
    )
    print(query_user)
    await database.execute(query_user)
    data_new_user = await database.fetch_one(user.select().where(user.c.username == data_user.username))
    print(data_new_user)
    query_user_details = user_details.insert().values(
        user_id=dict(data_new_user.items())['id'],
        name=data_user.name,
        surname=data_user.surname,
        patronymic=data_user.patronymic,
        city=data_user.city,
        age=data_user.age,
        about_me=data_user.about_me
    )
    print(query_user_details)
    await database.execute(query_user_details)
    return data_user


@router.get("/{user_id}/posts", response_model=List[ShowPost])
def show_user_posts(user_id: int):
    query = select([post.c.id, post.c.post_title, post.c.post_slug, post.c.content]). \
        select_from(user.join(post)). \
        where(user.c.id == user_id)
    print(query)
    posts = database.execute(query)
    print(posts)
    return posts.fetchall()
