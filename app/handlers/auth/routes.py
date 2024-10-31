from fastapi import APIRouter, HTTPException, status
from app.handlers.auth.schemas import UserCreate, UserResponse
from app.handlers.auth.repo import UserRepo
from app.db.main import db_session

auth_router = APIRouter()
user_repo = UserRepo()

@auth_router.post(
        "/signup",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED
        )
async def create_user(user_data: UserCreate, session: db_session):
    email = user_data.email
    user_exists = await user_repo.user_exists(session, email=email)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already in use")
    
    new_user = await user_repo.create_user(user_data, session)
    return UserResponse.model_validate(new_user)