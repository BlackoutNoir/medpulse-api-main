from typing import List, Optional
from app.db.models import Department 
from app.db.main import db_session
from app.entities.department.schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentFilter
from sqlmodel import select, and_


class DepartmentRepo:

    async def get_all_departments(self, session: db_session) -> List[DepartmentResponse]:
        statement = select(Department)
        result = await session.execute(statement)
        depts = result.scalars().all()

        return [DepartmentResponse.model_validate(dept) for dept in depts]
    
    async def get_department(self, department_id: str, session: db_session) -> Optional[DepartmentResponse]:
        statement = select(Department).where(Department.uid == department_id)
        result = await session.execute(statement)
        department = result.scalars().one_or_none()

        return DepartmentResponse.model_validate(department) if department else None
    
    async def create_department(self, department_data: DepartmentCreate, session: db_session) -> DepartmentResponse:
      
        new_department = Department(**department_data.model_dump())
        session.add(new_department)
        await session.commit()
        await session.refresh(new_department)

        return DepartmentResponse.model_validate(new_department)
    
    async def update_department(self, department_id: str, department: DepartmentUpdate, session: db_session) -> DepartmentResponse:
        statement = select(Department).where(Department.uid == department_id)
        result = await session.execute(statement)
        department_to_update = result.scalars().one_or_none()

        if not department_to_update:
            return None

        for key, value in department.model_dump(exclude_unset=True).items():
            setattr(department_to_update, key, value) 
            
        

        await session.commit()
        await session.refresh(department_to_update)
        return DepartmentResponse.model_validate(department_to_update)
    
    async def delete_department(self, department_id: str, session: db_session) -> bool:
        statement = select(Department).where(Department.uid == department_id)
        result = await session.execute(statement)
        department_to_delete= result.scalars().one_or_none()
        if not department_to_delete:
            return False
        await session.delete(department_to_delete)
        await session.commit()
        return True 
    

    async def filter_departments(self, filters: DepartmentFilter, session: db_session) -> List[DepartmentResponse]:

        statement = select(Department)
        

        partial_match_fields = [
            "uuid","name","description"
            ]


        conditions = []
        for field, value in filters.model_dump(exclude_none=True).items():
            if field == "order_by":
                continue
            column = getattr(Department, field)
            if field in partial_match_fields and isinstance(value, str):
                conditions.append(column.ilike(f"%{value}%"))
            else:
                conditions.append(column == value)


        if conditions:
            statement = statement.where(and_(*conditions))

        
        if filters.order_by and hasattr(Department, filters.order_by):
            order_column = getattr(Department, filters.order_by)
            statement = statement.order_by(order_column)

        result = await session.execute(statement)
        depts = result.scalars().all()

        return [DepartmentResponse.model_validate(dept) for dept in depts]