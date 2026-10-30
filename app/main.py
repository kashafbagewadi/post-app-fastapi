from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
async def main():
    return {"message": "Hello from Blog Post App - powered by FastAPI!!!"}

