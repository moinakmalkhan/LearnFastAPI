from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, utils
from database import get_db
import oauth2


router = APIRouter()

@router.post("/login", response_model=schemas.TokenWithUser)
def login(user_credientils: schemas.User, db: Session = Depends(get_db)):
    user: schemas.UserDetail = db.query(models.User).filter(models.User.email == user_credientils.email).first()
    if not user or not utils.verify_password(user_credientils.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    return {
        'token': oauth2.create_access_token({'user_id': user.id}),
        'token_type': 'bearer',
        'user': user
        }
    