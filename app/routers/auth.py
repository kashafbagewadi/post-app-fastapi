from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db
from .. import models, schemas, utils

router = APIRouter(tags=['Authentication'])

@router.post('/login')
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    # create a token

    # return a token