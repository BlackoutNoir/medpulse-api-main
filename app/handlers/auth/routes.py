from fastapi import APIRouter, HTTPException, status
from app.handlers.auth.schemas import UserCreate, UserResponse, UserLogin
from app.handlers.auth.repo import UserRepo
from app.db.main import db_session
from app.handlers.auth.utils import decode_token, create_access_token, verify_passwd
from datetime import timedelta
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_repo = UserRepo()

REFRESH_TOKEN_EXPIRY = 2

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


@auth_router.post(
        "/login",
        )
async def login(user_data: UserLogin, session: db_session):   
    
    if user_data.email:
        user = await user_repo.get_user_by_email(user_data.email, session)
    else:
        user = await user_repo.get_user_by_username(user_data.username, session)

    if user is not None:
        password_valid = verify_passwd(user_data.password, user.password_hash)

        if password_valid:
            access_token=create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)   
                },
            )
            
            refresh_token=create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid)   
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message" : "Login successful",
                    "access_token" : refresh_token,
                    "refresh_token" : refresh_token,
                    "user" : {
                        "email" : user.email,
                        "user_uid" : str(user.uid)
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")        