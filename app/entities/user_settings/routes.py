from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.user_settings.repo import UserSettingsRepo
from app.entities.user_settings.schema import SettingsResponse, SettingsCreate, SettingsUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

user_settings_router = APIRouter()
repo = UserSettingsRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@user_settings_router.get("/", response_model=List[SettingsResponse],
                          )
async def get_all_settings(session: db_session,   user_details: access_token_bearer):
    return await UserSettingsRepo().get_all_settings(session)


@user_settings_router.get("/{settings_id}", response_model=SettingsResponse)
async def get_setting(settings_id: str, session: db_session, user_details: access_token_bearer):
    print(user_details)
    settings =  await UserSettingsRepo().get_setting(settings_id, session)
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    
    return settings

@user_settings_router.post("/", response_model=SettingsResponse, status_code=status.HTTP_201_CREATED)
async def create_setting(setting: SettingsCreate, session: db_session, user_details: access_token_bearer):
    return await UserSettingsRepo().create_setting(setting, session)


@user_settings_router.put("/{settings_id}", response_model=SettingsResponse)
async def update_setting(settings_id: str, setting: SettingsUpdate, session: db_session,  user_details: access_token_bearer):    
    settings = await UserSettingsRepo().get_setting(settings_id, session)
    
    if not settings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")
    return await UserSettingsRepo().update_setting(settings_id, setting, session)


@user_settings_router.delete("/{settings_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(settings_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await UserSettingsRepo().delete_setting(settings_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Settings not found")  
    return 
