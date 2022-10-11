from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models




oauth_scheme = OAuth2PasswordBearer(tokenUrl='login', auto_error=True)

SECRET_KEY = "$2b$12$9nOUd6kQuNuI5acS/ls8hOpjhwTw3SSSblahSG1p6FzPBCLv.BVAu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode['exp'] = datetime.utcnow() +  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def verify_access_token(token: str, exception):
    try:
        user_id: str = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get('user_id')
        if user_id is None:
            raise exception
        return user_id
    except JWTError:
        raise exception

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token, HTTPException(status.HTTP_401_UNAUTHORIZED, "Could validate credentials", headers={
        'WWW-Authenticate': 'Bearer'
    }))
    return db.query(models.User).filter(models.User.id == user_id).first()


