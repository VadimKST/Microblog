import uvicorn
from fastapi import FastAPI

from app.routers import post, user


app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
def index():
    return {"message": "main_page"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
