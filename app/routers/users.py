from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_new_user(user: schemas.User, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    new_user = models.User(**user.model_dump())
    new_user.password = utils.hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found!")
    return user