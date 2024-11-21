from fastapi import APIRouter, HTTPException, status
from typing import List
from app.db.main import db_session
from app.entities.department.repo import DepartmentRepo
from app.entities.department.schema import DepartmentResponse, DepartmentCreate, DepartmentUpdate, DepartmentFilter
from app.handlers.auth.dependencies import access_token_bearer, RoleChecker


# admin_role_checker = Depends(RoleChecker(['admin']))
department_router = APIRouter()
repo = DepartmentRepo()

@department_router.get("/", response_model=List[DepartmentResponse], status_code=status.HTTP_200_OK)
async def get_all_Departments(session: db_session,   user_details: access_token_bearer):
    return await repo.get_all_departments(session)

@department_router.get("/{department_id}", response_model=DepartmentResponse, status_code=status.HTTP_200_OK)
async def get_department(department_id: str, session: db_session, user_details: access_token_bearer):
    dept =  await repo.get_department(department_id, session)
    if not dept:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="department not found")
    
    return dept


@department_router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(department: DepartmentCreate, session: db_session, user_details: access_token_bearer):
    return await repo.create_department(department, session)

@department_router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(department_id: str, updated_department: DepartmentUpdate, session: db_session,  user_details: access_token_bearer):    
    department = await repo.get_department(department_id, session)
    
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    return await repo.update_department(department_id, updated_department, session)


@department_router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: str, session: db_session,  user_details: access_token_bearer):
    deleted = await repo.delete_department(department_id, session)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")  
    return 

@department_router.post("/filtered-departments", response_model=List[DepartmentResponse])
async def get_filtered_department(session: db_session, filters: DepartmentFilter):
    return await repo.filter_departments(filters, session)
