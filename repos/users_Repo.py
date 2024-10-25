from sqlalchemy.orm import Session
from models import User
from schema import UserCreate, UserUpdate  
from base_Repo import BaseRepo
from typing import Optional
import uuid


class UserRepo(BaseRepo):
    def __init__(self, db: Session):
        super().__init__(User, db)

    # Additional methods specific to users can be added here
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
