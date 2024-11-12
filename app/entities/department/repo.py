from typing import List, Optional
from app.db.models import Department
from app.db.main import db_session
from app.entities.department.schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from sqlmodel import select

class DepartmentRepo:

    async def get_all_department(self, session: db_session) -> List[DepartmentResponse]:
        statement = select(Department)
        result = await session.execute(statement)
        Department = result.scalars().all()

        return [DepartmentResponse.model_validate(Department) for Department in Department]
    
    async def get_department(self, Department_id: str, session: db_session) -> Optional[DepartmentResponse]:
        statement = select(Department).where(Department.uid == Department_id)
        result = await session.execute(statement)
        Department = result.scalars().one_or_none()

        return DepartmentResponse.model_validate(Department) if Department else None

    async def create_department(self, Department_data: DepartmentCreate, session: db_session) -> DepartmentResponse:
        new_Department = Department(**Department_data.model_dump())
        session.add(new_Department)
        await session.commit()
        await session.refresh(new_Department)
        return DepartmentResponse.model_validate(new_Department)
    
    async def update_department(self, Department_id: str, Department: DepartmentUpdate, session: db_session) -> DepartmentResponse:
        statement = select(Department).where(Department.uid == Department_id)
        result = await session.execute(statement)
        Department_to_update = result.scalars().one_or_none()

        if not Department_to_update:
            return None

        for key, value in Department.model_dump(exclude_unset=True).items():
            setattr(Department_to_update, key, value) 

        await session.commit()
        await session.refresh(Department_to_update)
        return DepartmentResponse.model_validate(Department_to_update)
    
    async def delete_department(self, Department_id: str, session: db_session) -> bool:
        statement = select(Department).where(Department.uid == Department_id)
        result = await session.execute(statement)
        Department_to_delete= result.scalars().one_or_none()
        if not Department_to_delete:
            return False
        await session.delete(Department_to_delete)
        await session.commit()
        return True
    
