from typing import List, Optional, Union
from app.db.models import User
from app.db.main import db_session
from app.entities.user.schema import UserResponse, UserCreate, UserUpdate, UserFilter
from app.entities.user.service import UserService 
from app.handlers.auth.schemas import UserCreate
from sqlmodel import select, and_
from datetime import datetime

user_service = UserService()


class UserRepo:

    async def get_all_users(self, session: db_session) -> List[UserResponse]:
        statement = select(User)
        result = await session.execute(statement)
        users = result.scalars().all()

        return [UserResponse.model_validate(user) for user in users]
    
    async def get_user(self, user_id: str, session: db_session) -> Optional[UserResponse]:
        statement = select(User).where(User.uid == user_id)
        result = await session.execute(statement)
        user = result.scalars().one_or_none()

        return UserResponse.model_validate(user) if user else None
    
    async def create_user(self, user_data: Union[UserCreate], session: db_session) -> UserResponse:
      
        new_user = User(**user_data.model_dump(exclude={"settings"}))
        new_user.password_hash = user_service.hash_passwd(user_data.password)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        await user_service.create_user_settings(new_user.uid, session)

        await session.refresh(new_user)

        return UserResponse.model_validate(new_user)
    
    async def update_user(self, user_id: str, user: UserUpdate, session: db_session) -> UserResponse:
        statement = select(User).where(User.uid == user_id)
        result = await session.execute(statement)
        user_to_update = result.scalars().one_or_none()

        if not user_to_update:
            return None

        for key, value in user.model_dump(exclude_unset=True, exclude={"settings"}).items():
            setattr(user_to_update, key, value) 
        
        if user.settings:
            for key,value in user.settings.model_dump(exclude_unset=True).items():
                setattr(user_to_update.settings, key, value)

        user_to_update.updated_at = datetime.now()

        await session.commit()
        await session.refresh(user_to_update)
        return UserResponse.model_validate(user_to_update)
    
    async def delete_user(self, user_id: str, session: db_session) -> bool:
        statement = select(User).where(User.uid == user_id)
        result = await session.execute(statement)
        user_to_delete= result.scalars().one_or_none()
        if not user_to_delete:
            return False
        await session.delete(user_to_delete)
        await session.commit()
        return True
    

    async def filter_users(self, filters: UserFilter, session: db_session) -> List[UserResponse]:

        statement = select(User)
        

        partial_match_fields = [
            "username", "email", "firstname", "lastname", 
            "phone_no", "date_of_birth","created_at","updated_at","last_login"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(User, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(User, filters.order_by):
            order_column = getattr(User, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        users = result.scalars().all()

        return [UserResponse.model_validate(user) for user in users]