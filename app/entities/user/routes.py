from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.user.repo import UserRepo
from app.entities.user.schema import UserResponse, UserCreate, UserUpdate, UserFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
user_router = APIRouter()
repo = UserRepo()

@user_router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_users(session)

@user_router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, session: db_session, user_details: access_token_bearer):
    user =  await repo.get_user(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    return user


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_user(user, session)

@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_user : UserUpdate, session: db_session,  user_details: access_token_bearer):    
    user = await repo.get_user(user_id, session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await repo.update_user(user_id, updated_user, session)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_user(user_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")  
    return 

@user_router.post("/filtered-users", response_model=List[UserResponse])
async def get_filtered_users(session: db_session, filters: UserFilter):
    return await repo.filter_users(filters, session)
