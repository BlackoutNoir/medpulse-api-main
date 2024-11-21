from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.staff.repo import StaffRepo
from app.entities.staff.schema import StaffResponse, StaffCreate, StaffUpdate, StaffFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
staff_router = APIRouter()
repo = StaffRepo()

@staff_router.get("/", response_model=List[StaffResponse], status_code=status.HTTP_200_OK)
async def get_all_Staffs(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_staffs(session)

@staff_router.get("/{staff_id}", response_model=StaffResponse, status_code=status.HTTP_200_OK)
async def get_staff(staff_id: str, session: db_session, user_details: access_token_bearer):
    staff =  await repo.get_staff(staff_id, session)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="staff not found")
    
    return staff


@staff_router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(staff: StaffCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_staff(staff, session)

@staff_router.put("/{staff_id}", response_model=StaffResponse)
async def update_staff(staff_id: str, updated_staff: StaffUpdate, session: db_session,  user_details: access_token_bearer):    
    staff = await repo.get_staff(staff_id, session)
    
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    return await repo.update_staff(staff_id, updated_staff, session)


@staff_router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(staff_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_staff(staff_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")  
    return 

@staff_router.post("/filtered-staffs", response_model=List[StaffResponse])
async def get_filtered_staff(session: db_session, filters: StaffFilter):
    return await repo.filter_staffs(filters, session)