from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, oauth2

router = APIRouter()

@router.get("/",  response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db), user: schemas.UserDetail = Depends(oauth2.get_current_user)):
    print(user.dict())
    return db.query(models.Post).all()

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")
    return post

@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db), user: schemas.UserDetail = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{post_id}", status_code=202, response_model=schemas.Post)
def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db), user: schemas.UserDetail = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id)
    if not db_post.first():
        raise HTTPException(404, f"Post not found with id {post_id}")
    db_post.update(post)
    db.commit()
    return db_post.first()


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id)
    if not db_post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.delete(synchronize_session=False)
    db.commit()
    return

