import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database
from app.routers import post, user

app = FastAPI(title="Microblog")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)


@app.on_event("startup")
async def startup():
    print("Startup is running")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Shutdown is running")
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
