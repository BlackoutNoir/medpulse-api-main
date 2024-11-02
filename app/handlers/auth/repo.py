from typing import List, Optional
from app.handlers.auth.models import User
from app.db.main import db_session
from app.handlers.auth.schemas import UserCreate, UserResponse
from sqlmodel import select, or_
from app.handlers.auth.utils import generate_passwd_hash, verify_passwd, decode_token, create_access_token


class UserRepo:

    async def get_user_by_email(self,email: str, session: db_session) -> User:       
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().one_or_none()
        return user
    
    async def get_user_by_username(self,username: str, session: db_session) -> User:       
        statement = select(User).where(User.username == username)
        result = await session.execute(statement)
        user = result.scalars().one_or_none()
        return user
    
    async def user_exists(self, session: db_session,email: Optional[str] = None,username :Optional[str] = None,) -> bool:
        
        if not email and not username:
            raise ValueError("Either email or username must be provided")

        statement = select(User)
        if email and username:
            statement = statement.where(or_(User.email == email, User.username == username))
        elif email:
            statement = statement.where(User.email == email)
        else:
            statement = statement.where(User.username == username)

        result = await session.execute(statement)
        user = result.scalars().one_or_none()

        return user is not None
    

    async def create_user(self, user_data: UserCreate, session: db_session) -> UserResponse:
        new_user = User(**user_data.model_dump())
        new_user.password_hash = generate_passwd_hash(user_data.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserResponse.model_validate(new_user)