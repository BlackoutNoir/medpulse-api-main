from app.entities.user.repo import UserRepo
from app.db.main import db_session
from app.handlers.auth.schemas import UserResponse, UserCreate
from datetime import datetime 


user_repo = UserRepo()

class AuthService:

    async def create_user(self, user: UserCreate, session: db_session) -> UserResponse:
        return await user_repo.create_user(user, session)
        

