from typing import List, Optional
from app.db.models import Staff
from app.db.main import db_session
from app.entities.staff.schema import StaffCreate, StaffUpdate, StaffResponse
from sqlmodel import select

class StaffRepo:

    async def get_all_staff(self, session: db_session) -> List[StaffResponse]:
        statement = select(Staff)
        result = await session.execute(statement)
        Staff = result.scalars().all()

        return [StaffResponse.model_validate(Staff) for Staff in Staff]
    
    async def get_staff(self, Staff_id: str, session: db_session) -> Optional[StaffResponse]:
        statement = select(Staff).where(Staff.uid == Staff_id)
        result = await session.execute(statement)
        Staff = result.scalars().one_or_none()

        return StaffResponse.model_validate(Staff) if Staff else None

    async def create_staff(self, Staff_data: StaffCreate, session: db_session) -> StaffResponse:
        new_Staff = Staff(**Staff_data.model_dump())
        session.add(new_Staff)
        await session.commit()
        await session.refresh(new_Staff)
        return StaffResponse.model_validate(new_Staff)
    
    async def update_staff(self, Staff_id: str, Staff: StaffUpdate, session: db_session) -> StaffResponse:
        statement = select(Staff).where(Staff.uid == Staff_id)
        result = await session.execute(statement)
        Staff_to_update = result.scalars().one_or_none()

        if not Staff_to_update:
            return None

        for key, value in Staff.model_dump(exclude_unset=True).items():
            setattr(Staff_to_update, key, value) 

        await session.commit()
        await session.refresh(Staff_to_update)
        return StaffResponse.model_validate(Staff_to_update)
    
    async def delete_staff(self, Staff_id: str, session: db_session) -> bool:
        statement = select(Staff).where(Staff.uid == Staff_id)
        result = await session.execute(statement)
        Staff_to_delete= result.scalars().one_or_none()
        if not Staff_to_delete:
            return False
        await session.delete(Staff_to_delete)
        await session.commit()
        return True
    
