from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models import User
from backend.database import get_db

router = APIRouter()

@router.post("/users/")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{user_id}")
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
