from typing import List

from fastapi import HTTPException, APIRouter, Depends

from db import database
from core.models.model import post
from core.schemas.schemes import AddPost, UpdatePost, ShowPost, ShowUser
from app import dependencies

router = APIRouter(prefix="/post")


@router.post("/create", status_code=201)
async def create_post(data_post: AddPost, current_user: dict = Depends(dependencies.get_current_user)):
    query = post.insert().values(
        post_title=data_post.post_title,
        post_slug=data_post.post_slug,
        content=data_post.content,
        user_id=current_user["id"]
    )
    print(query)
    await database.execute(query)
    return data_post


@router.put("/update/{post_id}")
async def update_post(
        post_id: int,
        new_data_post: UpdatePost,
        current_user: dict = Depends(dependencies.get_current_user)
):
    update_query = post.update().values(**new_data_post.dict(exclude_unset=True)).where(post.c.id == post_id)
    data_post = await database.fetch_one(post.select().where(post.c.id == post_id))
    if data_post and dict(data_post.items())["user_id"] == current_user["id"]:
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
