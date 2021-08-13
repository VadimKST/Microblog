from typing import List

from fastapi import HTTPException, APIRouter

from db import connection
from core.models.model import post
from core.schemas.schemes import AddPost, UpdatePost, ShowPost


router = APIRouter(prefix="/post")


@router.post("/add_post")
def add_post(data_post: AddPost):
    query = post.insert().values(
        post_title=data_post.post_title,
        post_slug=data_post.post_slug,
        content=data_post.content
    )
    print(query)
    connection.execute(query)
    return data_post


@router.put("/update_post/{post_id}")
def update_post(post_id: str, data_post: UpdatePost):
    update_query = post.update().values(**data_post.dict(exclude_unset=True)).where(post.c.id == post_id)
    if connection.execute(post.select().where(post.c.id == post_id)).fetchone():
        return connection.execute(update_query)
    else:
        raise HTTPException(status_code=404, detail="Такого поста не существует")


@router.get("/show_post/{post_id}", response_model=ShowPost)
def show_post(post_id: int):
    query = post.select().where(post.c.id == post_id)
    print(query)
    one_post = connection.execute(query).fetchone()
    if one_post:
        return one_post
    else:
        raise HTTPException(status_code=404, detail="Такого поста не существует")


@router.get("/show_posts", response_model=List[ShowPost])
def show_posts():
    query = post.select()
    print(query)
    posts = connection.execute(query)
    print(posts)
    return posts.fetchall()

# @app.post("/items/{item}")
# async def index(
#         item: int = Path(..., ge=1),
#         q: List[str] = Query(...),
#         size: float = Query(..., gt=0, lt=10),
#         user: str = Body(...)
# ):
#     query_items = {"item": item, "q": q, 'size': size, 'user': user}
#     return query_items


# @app.post("/post")
# async def post_test(
#         data_post: PostList,
#         ads_id: Optional[str] = Cookie(None),
#         pokie: Optional[str] = Header(None)
# ):
#     return {"data_post": data_post,
#             "ads_id": ads_id,
#             "pokie": pokie
#             }
