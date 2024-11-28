from fastapi import APIRouter, HTTPException, status, Depends
from app.handlers.auth.schemas import UserCreate, UserResponse, UserLogin
from app.handlers.auth.repo import AuthRepo
from app.handlers.auth.service import AuthService
from app.db.main import db_session
from app.handlers.auth.utils import decode_token, create_access_token, verify_passwd
from datetime import timedelta
from fastapi.responses import JSONResponse
from app.handlers.auth.dependencies import refresh_token_bearer, access_token_bearer
from datetime import datetime
from app.db.blocklist import add_jti_to_blocklist
from app.handlers.auth.dependencies import get_current_user


auth_router = APIRouter()
auth_repo = AuthRepo()
auth_service = AuthService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post(
        "/signup",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED
        )
async def create_user(user_data: UserCreate, session: db_session):
    email = user_data.email
    user_exists = await auth_repo.user_exists(session, email=email)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already in use")
    
    user_exists = await auth_repo.user_exists(session, username=user_data.username)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username already in use")

    new_user = await auth_service.create_user(user_data, session)
    return UserResponse.model_validate(new_user)


@auth_router.post(
        "/login",
        )
async def login(user_data: UserLogin, session: db_session):   
    
    if user_data.email:
        user = await auth_repo.get_user_by_email(user_data.email, session)
    else:
        user = await auth_repo.get_user_by_username(user_data.username, session)

    if user is not None:
        password_valid = verify_passwd(user_data.password, user.password_hash)

        if password_valid:
            access_token=create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "user_type" : user.user_type 
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

            await auth_repo.update_last_login(user.uid, session)

            return JSONResponse(
                content={
                    "message" : "Login successful",
                    "access_token" : access_token,
                    "refresh_token" : refresh_token,
                    "user" : {
                        "email" : user.email,
                        "user_uid" : str(user.uid)
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") 



@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: refresh_token_bearer):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@auth_router.get("/logout")
async def revoke_token(token_details: access_token_bearer):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )

@auth_router.get("/current")
async def get_current_user(user: get_current_user):
    return user