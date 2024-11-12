from fastapi import APIRouter, HTTPException, status, Depends
from typing import List,Annotated
from app.db.main import db_session
from app.entities.department.repo import DepartmentRepo
from app.entities.department.schema import DepartmentResponse, DepartmentCreate, DepartmentUpdate
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker

Department_router = APIRouter()
repo = DepartmentRepo()
# admin_role_checker = Depends(RoleChecker(['admin']))

@Department_router.get("/", response_model=List[DepartmentResponse],
                          )
async def get_alldepartment(session: db_session,   _details: access_token_bearer):
    return await DepartmentRepo().get_alldepartment(session)


@Department_router.get("/{Department_id}", response_model=DepartmentResponse)
async def get_department(Department_id: str, session: db_session, _details: access_token_bearer):
    print(_details)
    Department =  await DepartmentRepo().get_department(Department_id, session)
    if not Department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    return Department

@Department_router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(Department: DepartmentCreate, session: db_session, _details: access_token_bearer):
    return await DepartmentRepo().create_department(Department, session)


@Department_router.put("/{Department_id}", response_model=DepartmentResponse)
async def update_department(Department_id: str, Department: DepartmentUpdate, session: db_session,  _details: access_token_bearer):    
    Department = await DepartmentRepo().get_department(Department_id, session)
    
    if not Department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return await DepartmentRepo().update_department(Department_id, Department, session)


@Department_router.delete("/{Department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(Department_id: str, session: db_session,  _details: access_token_bearer):
    deleted = await DepartmentRepo().delete_department(Department_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")  
    return 
