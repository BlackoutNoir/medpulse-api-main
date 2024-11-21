from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.role.repo import RoleRepo
from app.entities.role.schema import RoleResponse, RoleCreate, RoleUpdate, RoleFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
role_router = APIRouter()
repo = RoleRepo()

@role_router.get("/", response_model=List[RoleResponse], status_code=status.HTTP_200_OK)
async def get_all_roles(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_roles(session)

@role_router.get("/{role_id}", response_model=RoleResponse, status_code=status.HTTP_200_OK)
async def get_role(role_id: str, session: db_session, user_details: access_token_bearer):
    role =  await repo.get_role(role_id, session)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role not found")
    
    return role


@role_router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(role: RoleCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_role(role, session)

@role_router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: str, updated_role : RoleUpdate, session: db_session,  user_details: access_token_bearer):    
    role = await repo.get_role(role_id, session)
    
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    return await repo.update_role(role_id, updated_role, session)


@role_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_role(role_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")  
    return 

@role_router.post("/filtered-roles", response_model=List[RoleResponse])
async def get_filtered_roles(session: db_session, filters: RoleFilter):
    return await repo.filter_roles(filters, session)
