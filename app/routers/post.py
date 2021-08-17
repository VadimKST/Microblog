from typing import List

from fastapi import HTTPException, APIRouter

from db import database
from core.models.model import post
from core.schemas.schemes import AddPost, UpdatePost, ShowPost


router = APIRouter(prefix="/post")


@router.post("/create", status_code=201)
async def create_post(data_post: AddPost):
    query = post.insert().values(
        post_title=data_post.post_title,
        post_slug=data_post.post_slug,
        content=data_post.content,
        user_id=data_post.user_id
    )
    print(query)
    await database.execute(query)
    return data_post


@router.put("/update/{post_id}")
async def update_post(post_id: int, data_post: UpdatePost):
    update_query = post.update().values(**data_post.dict(exclude_unset=True)).where(post.c.id == post_id)
    if await database.fetch_one(post.select().where(post.c.id == post_id)):
        return await database.execute(update_query)
    else:
        raise HTTPException(status_code=404, detail="Такого поста не существует")


@router.get("/{post_id}", response_model=ShowPost)
async def show_one_post(post_id: int):
    query = post.select().where(post.c.id == post_id)
    print(query)
    one_post = await database.fetch_one(query)
    if one_post:
        return one_post
    else:
        raise HTTPException(status_code=404, detail="Такого поста не существует")


@router.get("/all/", response_model=List[ShowPost])
async def show_all_posts():
    query = post.select()
    print(query)
    return await database.fetch_all(query)
