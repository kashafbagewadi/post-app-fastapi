from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from .. database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])

# # Get all posts of self owners
# @router.get("/", response_model=List[schemas.PostResponse])
# def get_all_posts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     return posts

# # Get posts using query parameters like limit (default 10), skip, search for paging features
# @router.get("/", response_model=List[schemas.PostResponse])
# def get_all_posts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user), limit: int = 1, skip: int = 0, search: Optional[str] = ""):
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return posts

# Get all posts with number of votes using SQL Left Outer Join query between Posts and Votes tables
@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_new_post(post: schemas.PostRequest, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get a specific post
@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")
    return post

# Delete the post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update the post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostRequest, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found!")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action!")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return updated_post