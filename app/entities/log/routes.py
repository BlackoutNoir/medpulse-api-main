from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.log.repo import LogRepo
from app.entities.log.schema import LogResponse, LogCreate, LogUpdate, LogFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
log_router = APIRouter()
repo = LogRepo()

@log_router.get("/", response_model=List[LogResponse], status_code=status.HTTP_200_OK)
async def get_all_logs(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_logs(session)

@log_router.get("/{log_id}", response_model=LogResponse, status_code=status.HTTP_200_OK)
async def get_log(log_id: str, session: db_session, user_details: access_token_bearer):
    log =  await repo.get_log(log_id, session)
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="log not found")
    
    return log


@log_router.post("/", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(log: LogCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_log(log, session)

@log_router.put("/{log_id}", response_model=LogResponse)
async def update_log(log_id: str, updated_log : LogUpdate, session: db_session,  user_details: access_token_bearer):    
    log = await repo.get_log(log_id, session)
    
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    
    return await repo.update_log(log_id, updated_log, session)


@log_router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(log_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_log(log_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")  
    return 

@log_router.post("/filtered-logs", response_model=List[LogResponse])
async def get_filtered_logs(session: db_session, filters: LogFilter):
    return await repo.filter_logs(filters, session)
