from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.log.repo import LogRepo
from app.entities.log.schema import LogResponse, LogCreate, LogUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

log_router = APIRouter()
repo = LogRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@log_router.get("/", response_model=List[LogResponse],
                          )
async def get_alllog(session: db_session,   _details: access_token_bearer):
    return await LogRepo().get_alllog(session)


@log_router.get("/{Log_id}", response_model=LogResponse)
async def get_setting(Log_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Log =  await LogRepo().get_setting(Log_id, session)
    if not Log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    
    return Log

@log_router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_setting(setting: LogCreate, session: db_session, _details: access_token_bearer):
    return await LogRepo().create_setting(setting, session)


@log_router.put("/{Log_id}", response_model=LogResponse)
async def update_setting(Log_id: str, setting: LogUpdate, session: db_session,  _details: access_token_bearer):    
    Log = await LogRepo().get_setting(Log_id, session)
    
    if not Log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    return await LogRepo().update_setting(Log_id, setting, session)


@log_router.delete("/{Log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_setting(Log_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await LogRepo().delete_setting(Log_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")  
    return 
