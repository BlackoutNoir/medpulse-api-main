from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.admin.repo import AdminRepo
from app.entities.admin.schema import AdminResponse, AdminCreate, AdminUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Admin_router = APIRouter()
repo = AdminRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Admin_router.get("/", response_model=List[AdminResponse],
                          )
async def get_alladmin(session: db_session,   _details: access_token_bearer):
    return await AdminRepo().get_alladmin(session)


@Admin_router.get("/{Admin_id}", response_model=AdminResponse)
async def get_admin(Admin_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Admin =  await AdminRepo().get_admin(Admin_id, session)
    if not Admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    
    return Admin

@Admin_router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(Admin: AdminCreate, session: db_session, _details: access_token_bearer):
    return await AdminRepo().create_admin(Admin, session)


@Admin_router.put("/{Admin_id}", response_model=AdminResponse)
async def update_admin(Admin_id: str, Admin: AdminUpdate, session: db_session,  _details: access_token_bearer):    
    Admin = await AdminRepo().get_admin(Admin_id, session)
    
    if not Admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
    return await AdminRepo().update_admin(Admin_id, Admin, session)


@Admin_router.delete("/{Admin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(Admin_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await AdminRepo().delete_admin(Admin_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")  
    return 
