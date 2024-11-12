from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.staff.repo import StaffRepo
from app.entities.staff.schema import StaffResponse, StaffCreate, StaffUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Staff_router = APIRouter()
repo = StaffRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Staff_router.get("/", response_model=List[StaffResponse],
                          )
async def get_allstaff(session: db_session,   _details: access_token_bearer):
    return await StaffRepo().get_allstaff(session)


@Staff_router.get("/{Staff_id}", response_model=StaffResponse)
async def get_staff(Staff_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Staff =  await StaffRepo().get_staff(Staff_id, session)
    if not Staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    return Staff

@Staff_router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(Staff: StaffCreate, session: db_session, _details: access_token_bearer):
    return await StaffRepo().create_staff(Staff, session)


@Staff_router.put("/{Staff_id}", response_model=StaffResponse)
async def update_staff(Staff_id: str, Staff: StaffUpdate, session: db_session,  _details: access_token_bearer):    
    Staff = await StaffRepo().get_staff(Staff_id, session)
    
    if not Staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return await StaffRepo().update_staff(Staff_id, Staff, session)


@Staff_router.delete("/{Staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(Staff_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await StaffRepo().delete_staff(Staff_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")  
    return 
