from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils

router = APIRouter()

@router.post("/", response_model=schemas.UserDetail)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=schemas.UserDetail)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
