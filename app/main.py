from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware

# No need after Alembic, required for SQLAlchemy
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the domain of Frontend else ["*"] allows all domains
origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(votes.router)

@app.get("/")
async def main():
    return {"message": "Hello from Blog Post App - powered by FastAPI!!!"}

